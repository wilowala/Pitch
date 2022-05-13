from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,PasswordField,BooleanField,RadioField,ValidationError
from wtforms.validators import InputRequired,Email,EqualTo
from ..models import User

class Pitch(FlaskForm):

    pitch_category = RadioField('Label', choices=[ ('Business','Business'),('Life','Life'),('Education','Education'),('Technology','Technology')],validators=[InputRequired()])
    pitch_title = StringField('Pitch title',validators=[InputRequired()])
    pitch_descrip = TextAreaField('Pitch',validators=[InputRequired()])
    submit = SubmitField('Submit')

class Comment(FlaskForm):
    Comment_descrip =TextAreaField("Comment", validators=[InputRequired()])
    submit = SubmitField('Submit Comment')
    
class Upvote(FlaskForm):
    submit =SubmitField()

class Downvote(FlaskForm):
    submit =SubmitField()

class LoginForm(FlaskForm):
    email = StringField('Your Email Address',validators=[InputRequired(),Email()])
    password = PasswordField('Password',validators =[InputRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    email = StringField('Your Email Address',validators=[InputRequired(),Email()])
    username = StringField('Enter your username',validators = [InputRequired()])
    password = PasswordField('Password',validators = [InputRequired(), EqualTo('password_confirm',message = 'Passwords must match')])
    password_confirm = PasswordField('Confirm Passwords',validators = [InputRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self,data_field):
        if User.query.filter_by(email =data_field.data).first():
            raise ValidationError('There is an account with that email')

    def validate_username(self,data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('The username is taken')