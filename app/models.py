from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id=db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(20), unique=True, nullable=False)
	user_role=db.Column(db.String(20), unique=False)
	email=db.Column(db.String(120), unique=True, nullable=False)
	image_file=db.Column(db.String(20), nullable=False, default='default.jpg')
	password=db.Column(db.String(60),nullable=False)
	posts=db.relationship('Post', backref='author', lazy=True)

	def __repr__(self):
		return f"User('{self.username}',' {self.email}','{self.image_file}',' {self.user_role}')"

class Post(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	title=db.Column(db.String(100), nullable=False)
	subject=db.Column(db.String(25), nullable=False)
	post_type=db.Column(db.String(25), nullable=False)
	date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content=db.Column(db.Text, nullable=False)
	user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	
	def __repr__(self):
		return f"Post('{self.title}','{self.date_posted}')"

class Subjects(db.Model):
	course_id=db.Column(db.Integer, primary_key=True)
	course_code=db.Column(db.String(100), nullable=False)
	course_name=db.Column(db.String(100), nullable=False)
	assignments=db.relationship('Assignment', backref='course', lazy=True)
	def __repr__(self):
		return f"Subjects('{self.course_id}''{self.course_code}','{self.course_name}')"

class Assignment(db.Model):
	assignment_id=db.Column(db.Integer, primary_key=True)
	title=db.Column(db.String(100), nullable=False)
	content=db.Column(db.String(100), nullable=False)
	date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	due_date=db.Column(db.DateTime, nullable=True)
	submited_assigngments=db.relationship('SubmittedAssignment', backref='task', lazy=True)
	subject=db.Column(db.Integer, db.ForeignKey('subjects.course_id'), nullable=False)
	def __repr__(self):
		return f"Assignment('{self.title}','{self.content}','{self.subject}','{self.date_posted}')"

class SubmittedAssignment(db.Model):
	id=db.Column(db.Integer, primary_key=True)	
	student_name=db.Column(db.String(25))
	assignment=db.Column(db.String, db.ForeignKey('assignment.assignment_id'), nullable=False)
	title=db.Column(db.String, nullable=False)
	subject=db.Column(db.String, nullable=False)
	marks=db.Column(db.Integer, nullable=True)
	file=db.Column(db.Text, nullable=False)
	def __repr__(self):
		return f"SubmittedAssignment('{self.id}','{self.student_name}','{self.title}','{self.file}', '{self.marks}')"


