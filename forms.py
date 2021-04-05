from flask_wtf import FlaskForm
from wtforms import * 
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
    messageArea = TextAreaField('Message', validators=[DataRequired()])
    uploadImage = FileField('Choose file')
    messageSubmit = SubmitField('Post')

class AccountForm(FlaskForm):
    oldpassword = PasswordField('Old Password', validators=[DataRequired()]) 
    newpassword = PasswordField('New Password', validators=[DataRequired(), Length(min=6, max=6)]) 
    confirmpassword = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('newpassword', message='password must match')])
    accountSubmit = SubmitField('Change')

class UpdatePostForm(FlaskForm):
    postID = StringField('PostID')
    subject = StringField('Subject', validators=[DataRequired()], render_kw={"placeholder": "Subject"})
    messageArea = TextAreaField('Message', validators=[DataRequired()])
    uploadImage = FileField('Choose file')
    hasImage = BooleanField('Has image')
    messageSubmit = SubmitField('Post')