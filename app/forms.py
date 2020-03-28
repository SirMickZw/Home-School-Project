from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField,PasswordField, SubmitField, BooleanField, TextAreaField, RadioField, IntegerField
from wtforms.validators import DataRequired, length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
	username=StringField('Username', validators=[DataRequired(), length(min=2, max=20)])
	user_role = RadioField('You Are A', choices=[('Student','Student'),('Lecturer','Lecturer'), ('Parent','Parent')])
	email=StringField('Email', validators=[DataRequired(), Email()])
	password=PasswordField('Password', validators=[DataRequired()])
	confirm_password=PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit=SubmitField('Sign Up')

	def validate_username(self, username):
		user=User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username Not Available')
	def validate_email(self, email):
		user=User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email Address Not Available')

class LoginForm(FlaskForm):
	email=StringField('Email', validators=[DataRequired(), Email()])
	password=PasswordField('Password', validators=[DataRequired()])
	remember=BooleanField('Remember Me')
	submit=SubmitField('Login')

class UpdateAccountForm(FlaskForm):
	username=StringField('Username', validators=[DataRequired(), length(min=2, max=20)])
	email=StringField('Email', validators=[DataRequired(), Email()])
	picture=FileField('Update Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit=SubmitField('Update')
	def validate_username(self, username):
		if username.data!=current_user.username:
			user=User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Username Not Available')
	def validate_email(self, email):
		user=User.query.filter_by(email=email.data).first()
		if email.data!=current_user.email:
			if user:
				raise ValidationError('Email Address Not Available')

class PostForm(FlaskForm):
	title=StringField('Title', validators=[DataRequired	()])
	content=TextAreaField('Content', validators=[DataRequired()])
	submit=SubmitField('Post')
	post_type = RadioField('Post Type', choices=[('Assignment','Assignment'),('Test','Test'),('Notes','Notes'), ('Notice','Notice')])
	subject = RadioField('Subject', choices=[('Maths','Maths'),('Physics','Physics'), ('Chemistry','Chemistry'),('Biology','Biology'),('Accounts','Accounts'),('Geography','Geography'), ('English','English'), ('History','History')])
	attatchment=FileField('Attatch File', validators=[FileAllowed(['docx', 'pdf','doc', 'mp4'])])

class SubmitAssignmentForm(FlaskForm):
	title=StringField('Title', validators=[DataRequired	()])
	student_name=StringField('Student Name', validators=[DataRequired()])
	content=TextAreaField('Write Your Answer Here')
	submit=SubmitField('Submit ')
	attatchment=FileField('Attatch File', validators=[FileAllowed(['docx', 'pdf','doc', 'txt'])])

class AddGradesForm(FlaskForm):
	grade=IntegerField('Grades (%)', validators=	[DataRequired()])
	submit=SubmitField('Submit ')
