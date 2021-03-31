from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    userID = StringField('Login ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submitField = SubmitField('Login')


class RegistrationForm(FlaskForm):
    userID = StringField('Login ID', validators=[DataRequired(), Length(min=9, max=9)])
    username = StringField('Username', validators=[DataRequired()]) 
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=6)]) 
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='password must match')])
    uploadImage = FileField('Choose file')
    submitField = SubmitField('Register')

class MessageForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()], render_kw={"placeholder": "Subject"})
    messageArea = StringField('Message', validators=[DataRequired()], widget=TextArea())
    uploadImage = FileField('Choose file')
    submitField = SubmitField('Post')

class AccountForm(FlaskForm):
    # userID = StringField('Login ID', validators=[DataRequired(), Length(min=9, max=9)])
    # username = StringField('Username', validators=[DataRequired()]) 
    oldpassword = PasswordField('Old Password', validators=[DataRequired()]) 
    newpassword = PasswordField('New Password', validators=[DataRequired(), Length(min=6, max=6)]) 
    confirmpassword = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password', message='password must match')])
    uploadImage = FileField('Choose file')
    submitField = SubmitField('Register')