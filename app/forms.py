from flask_wtf import Form
from wtforms.validators import DataRequired, Required, ValidationError, Email, Length, EqualTo
from wtforms.fields import SubmitField, PasswordField, TextField, TextAreaField, StringField, BooleanField
from models import User
from app import db

class SignupForm(Form):
    nickname = TextField("User name",  validators=[DataRequired("Please enter your first name."), Length(min=4, max=20, message='User name must be between 4 and 20 haracters')])
    email = TextField("Email",  validators=[DataRequired("Please enter your email address."), Email("Please enter a valid email address.")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password.")])
    confirm = PasswordField('Repeat your password', validators = [EqualTo('password', message='Passwords must match')]) 
    submit = SubmitField("Create account")

    # def __init__(self, *args, **kwargs):
    #     Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        
        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True

class SigninForm(Form):
    email = TextField("Email",  validators=[DataRequired("Please enter your email address."), Email("Please enter a valid email address.")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password.")])
    submit = SubmitField("Login")
    remember_me = BooleanField('remember_me', default=False)

    # def __init__(self, *args, **kwargs):
    #     Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        
        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.email.errors.append("Invalid Email or Password")
            return False



