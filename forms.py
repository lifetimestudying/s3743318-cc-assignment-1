from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    userID = StringField('Login ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remeber Me')
    submitField = SubmitField('Login')


class RegistrationForm(FlaskForm):
    userID = StringField('Login ID', validators=[DataRequired(), Length(min=9, max=9)])
    username = StringField('Username', validators=[DataRequired()]) 
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=6)]) 
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='password must match')])
    submitField = SubmitField('Register')

