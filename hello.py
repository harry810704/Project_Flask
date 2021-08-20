from flask import Flask, render_template

# Create a Flask Instance
app = Flask(__name__)

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