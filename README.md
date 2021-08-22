# Project_Flask
This is a demo web app using flask

DATABASE
flask_sqlalchemy:
SQLAlchemy to connect to sqlite, mysql
  To create mysql db using create_db.py and don't forget to change password and db name

flask_migrate:
Migration for adding more data into database
  1. Adding name and form in class
  2. Terminal: flask db -m 'commit note'
  3. Terminal: flask db upgrade
  
FORM
wtf:
  Field to give label and properties:
    'string field'
    'password field'
    'submit field'
  'Datarequired' to check if the input is filled
  'EqualTo' to check if pw and confirm pw is matched
  'TextArea' give multiple line for input content area
  
'flash()' to give message after a button clicked

flask_login:
  'UserMixin' need to be in class of users
  'login_manager' = 'LoginManager()' flask login function
  'login_required' check if user is logged in to view the page
  'login_user' authorize the user for login status
  'logout_user' unauthorize the user for login status
  'current_user' contain the logged in user info
  
werkzeug:
  'generate_password_hash' encode pw into hash
  'check_password_hash' check the login pw to pw_hash in db
