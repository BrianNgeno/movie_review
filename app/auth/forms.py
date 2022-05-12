from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,PasswordField, BooleanField
from wtforms.validators import InputRequired,Email, EqualTo
from ..models import User
from wtforms import ValidationError
import email_validator

class Registration(FlaskForm):
    email = StringField('email address',validators=[InputRequired(), Email()])
    username = StringField('username',validators=[InputRequired()])
    password = PasswordField('enter you password',validators=[InputRequired(), EqualTo('password_confirm',message='Passwords must match')])
    password_confirm = PasswordField('confirm password')
    submit  = SubmitField('Register')

    def validate_username(self,data_field):
        if User.query.filter_by(username=data_field.data).first():
            raise ValidationError('Username is already taken try another one')

    def validate_email(self,data_field):
        if User.query.filter_by(email=data_field.data).first():
            raise ValidationError('There is an account with that email')

class LoginForm(FlaskForm):
    email = StringField('email address',validators=[InputRequired(), Email()])
    password = PasswordField('enter you password',validators=[InputRequired()])
    remember = BooleanField('Remember me')
    submit  = SubmitField('Sign In')