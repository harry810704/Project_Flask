from operator import methodcaller
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, SubmitField
from wtforms.fields.simple import PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from wtforms.widgets.core import TextArea
from flask_login import UserMixin, login_manager, login_user, LoginManager, login_required, logout_user, current_user

# Create a Flask Instance
app = Flask(__name__)

# Secret key
app.config['SECRET_KEY'] = "my super secret key"

# Add SQLAlchemy Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# Add MySQL Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/db'
# Initialize the Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Create User Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(120), nullable = False, unique = True)
    country = db.Column(db.String(100))
    date_added = db.Column(db.DateTime, default=datetime.now)
    # Do some password stuff!!
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.name

# Create a Account Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("User Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    country = StringField("Country")
    submit = SubmitField("Submit")

# Create a Name Form Class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a PW Form Class
class PasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a Blog Post model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.now)
    slug = db.Column(db.String(255))

# Create a Posts Form
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()], widget=TextArea())
    author = StringField('Author', validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    submit = SubmitField("Submit")

# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Create Login Form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a route decorator
@app.route('/')

# def index():
#     return "<h1>Hello world!</h1>"

# Filters for html import variable
# safe
# capitalize
# upper
# lower
# title
# trim
# striptags

def index():
    first_name = 'Harry'
    stuff = 'This is <strong>bold</strong> text'
    stuff_title = 'This is my flask project'
    drinks = ['coke', 'sprite', 'tea', 'coffee', 6]
    return render_template("index.html", first_name=first_name, stuff=stuff, stuff_title=stuff_title, drinks=drinks)

# Add Data Into Database
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash the password
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(username = form.username.data, name=form.name.data, email=form.email.data, country = form.country.data, password_hash = hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.country.data = ''
        form.password_hash = ''
        flash('User Added Successfully!!')
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name = name, our_users = our_users)

# Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.country = request.form['country']
        try:
            db.session.commit()
            flash("User Updated Successfully!!")
            return render_template("update.html", form = form, name_to_update = name_to_update)
        except:
            flash("Error! Looks like there was a problem")
            return render_template("update.html", form = form, name_to_update = name_to_update)
    else:
        return render_template("update.html", form = form, name_to_update = name_to_update, id = id)

# Delete Data from Database
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!!")

        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html", form = form, name = name, our_users = our_users)

    except:
        flash("Whoops! There was a problem deleting user, try again...")
        return render_template("add_user.html", form = form, name = name)

# localhost:5000/user/name
@app.route('/user/<name>')

def user(name):
    return render_template("user.html", user_name=name)

# Invalid URL
@app.errorhandler(404)

def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)

def page_not_found(e):
    return render_template("500.html"), 500

# Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successful")
    return render_template("name.html", name = name, form = form)

# Create Password Test Page
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        # Clear the form
        form.email.data = ''
        form.password_hash.data = ''
        # Look up User By Email
        pw_to_check = Users.query.filter_by(email=email).first()
        # Check Hassed Password
        passed = check_password_hash(pw_to_check.password_hash, password)
        # flash("Form Submitted Successful")

    return render_template("test_pw.html", email = email, password = password, pw_to_check = pw_to_check, passed = passed, form = form)

# Add Post Page
@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    title = None
    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data, author=form.author.data, slug=form.slug.data)
        title = form.title.data
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''

        # Add post data to database
        db.session.add(post)
        db.session.commit()

        # Return a Message
        flash("Blog Post Submitted Successfully!!")
    our_posts = Posts.query.order_by(Posts.date_posted)
    # Redirect to the webpage
    return render_template('add_post.html', form = form, title = title, our_posts = our_posts)

@app.route('/post')
def posts():
    # Grab all the posts from the database
    our_posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", our_posts = our_posts)

# Delete Data from Database
@app.route('/post/delete/<int:id>')
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Post Deleted Successfully!!")

        our_posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", our_posts = our_posts)

    except:
        flash("Whoops! There was a problem deleting post, try again...")
        return render_template("posts.html", our_posts = our_posts)

@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post = post)

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        # Update Database
        db.session.add(post)
        db.session.commit()
        flash("Post Has Been Updated!")
        return redirect(url_for('post', id=post.id))
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('edit_post.html', form = form)

# Create Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user =Users.query.filter_by(username=form.username.data).first()
        if user:
            #check the hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Successfully!!")
                return redirect(url_for('dashboard'))
            else:
                flash("Worng Password - Try Again!!")
        else:
            flash("That User Doesn't Exist - Try Again!!")
    return render_template('login.html', form = form)

# Create Logout Page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out! Thanks For Stopping By!")
    return redirect(url_for('login'))

# Create Dashboard Page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

# Send json
@app.route('/date')
def get_current_date():
    favorite_pizza = {
        "John" : "Pepperoni",
        "Mary" : "Cheese",
        "Tim" : "Mushroom"
    }
    return favorite_pizza
    # return {"Date": date.today()}
