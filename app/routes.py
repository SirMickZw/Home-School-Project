import secrets
import os
import cv2
from io import BytesIO
import numpy as np 
from werkzeug.utils import secure_filename
from PIL import Image	
from flask import render_template, url_for, flash, redirect, request, abort, send_file
from app import app, db, bcrypt
from app.read_doc import ReadingTextDocument
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, SubmitAssignmentForm, AddGradesForm, SearchStudentForm
from app.models import User, Post, Subjects, Assignment, SubmittedAssignment
from flask_login import login_user, current_user, logout_user, login_required

ALLOWED_EXTENSIONS = ['txt', 'pdf', 'doc', 'docx', 'ppt', 'pptx']

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/home")
def home():
	if current_user.is_authenticated:
		image_file=url_for('static', filename='profile_pics/'+current_user.image_file)
		x=image_file
		form=SearchStudentForm()
		return render_template('dashboard.html', image_file='x', form=form)
	posts=Post.query.all()
	

	return render_template('home.html', posts=posts )

@app.route("/blog")
def blog():
	posts=Post.query.all()
	return render_template('home.html', posts=posts )

@app.route("/about")
def about():
    return render_template('about.html',title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form=RegistrationForm()
	if form.validate_on_submit():
		hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user=User(username=form.username.data, user_role=form.user_role.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Welcom {form.username.data}', 'success')
		return redirect('login')
	return render_template('register.html', title='Register', form=form )

@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page=request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('invalid email address or password', 'danger')
	return render_template('login.html', title='login', form=form )

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('login'))

def save_picture(form_picture):
	random_hex=secrets.token_hex(8)
	_, f_ext=os.path.splitext(form_picture.filename)
	picture_fn=random_hex+f_ext
	picture_path=os.path.join(app.root_path, 'static/profile_pics',picture_fn)
	output_size=(125,125)
	i=Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	form=UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			form_picture=save_picture(form.picture.data)
			current_user.image_file=form_picture
		current_user.username=form.username.data
		current_user.email=form.email.data
		db.session.commit()
		flash('Your Updates were Successfull!', 'success')
		return redirect(url_for('account'))
	elif request.method=='GET':
			form.username.data=current_user.username
			form.email.data=current_user.email
	image_file=url_for('static', filename='profile_pics/'+current_user.image_file)
	return render_template('account.html', title='Account',image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
	form=PostForm()
	if form.validate_on_submit():
		if form.post_type.data=='Notes':
			post=Post(post_type=form.post_type.data, subject=form.subject.data, title=form.title.data, content= form.content.data, author=current_user)
			db.session.add(post)
			db.session.commit()
			flash('Successfully Submited Post', 'success')
			return redirect(url_for('home'))
		elif form.post_type.data=='Assignment':
			post=Assignment( title=form.title.data, subject=form.subject.data, content= form.content.data)
			db.session.add(post)
			db.session.commit()
			flash('Successfully Uploaded Asignment', 'success')
			return redirect(url_for('home'))
	return render_template('creat_post.html', title='New Post', legend='Create New Post', form=form)

@app.route("/post/<int:post_id>")
@login_required
def post(post_id):
	post=Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
def update_post(post_id):
	post=Post.query.get_or_404(post_id)
	if post.author!=current_user:
		abort(403)
	form=PostForm()
	if form.validate_on_submit():
		post.title=form.title.data
		post.content=form.content.data
		db.session.commit()
		flash('Post Updated Succefully', 'success')
		return redirect(url_for('post', post_id=post.id))
	elif request.method=='GET':
		form.title.data=post.title
		form.content.data=post.content
	return render_template('creat_post.html', title='Update Post', legend='Upade Post', form=form)

@app.route("/post/<int:post_id>/delete", methods=[ 'POST'])
def delete_post(post_id):
	post=Post.query.get_or_404(post_id)
	if post.author!=current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Your POst has Been Deleted')
	return redirect(url_for('home'))

"""routes for subjects"""
@app.route("/classroom <int:course_id>", methods=['GET', 'POST'])
def classroom(course_id):
	subject=Subjects.query.get_or_404(course_id)
	tasks=Assignment.query.filter_by(subject=subject.course_name)
	posts=Post.query.filter_by(subject=subject.course_name).all()
	return render_template('classroom.html', suject=subject,tasks=tasks, posts=posts)

@app.route("/submit_assignment <int:assignment_id>", methods=['GET', 'POST'])
@login_required
def submit_assignment(assignment_id):
	task=Assignment.query.get_or_404(assignment_id)	
	sub=Subjects.query.get(task.subject)
	form=SubmitAssignmentForm()
	if form.validate_on_submit():
		fn=form.content.data
		sub=SubmittedAssignment(student_name=form.student_name.data, assignment=task.assignment_id, title=task.title, subject=task.subject, file=fn)
		db.session.add(sub)
		db.session.commit()
		flash('Your Assignment has been Succeffully', 'success')
		return redirect(url_for('home'))
	form.title.data=task.title
	form.student_name.data=current_user.username
	return render_template('submit_assignments.html', title='Upload Assignment', task=task, form=form)

@app.route("/update_assignment/<int:assignment_id>/update", methods=['GET', 'POST'])
def update_assignment(assignment_id):
	post=SubmittedAssignment.query.get_or_404(assignment_id)
	if post.student_name!=current_user.username:
		abort(403)
	form=SubmitAssignmentForm()
	if form.validate_on_submit():
		post.title=form.title.data
		post.file=form.content.data
		db.session.commit()
		flash('Assignment Updated Succefully', 'success')
		return redirect(url_for('home'))
	elif request.method=='GET':
		form.student_name.data=post.student_name
		form.title.data=post.title
		form.content.data=post.file
	return render_template('submit_assignments.html', title='Update Assignment', legend='Update Assignment', form=form)

@app.route("/assignments/SubmittedAssignment", methods=['POST', 'GET'])
@login_required
def ViewSubmited():
	ass=SubmittedAssignment.query.filter_by(student_name=current_user.username).all()
	lec=SubmittedAssignment.query.all()
	return render_template('submited.html', title='Submited',work=lec, file=ass)

@app.route("/mark_assignment/<int:post_id>", methods=['POST', 'GET'])
@login_required
def mark_assignment(post_id):
	if current_user.user_role!='Lecturer':
		abort(403)
	post=SubmittedAssignment.query.get_or_404(post_id)
	form=AddGradesForm()
	if form.validate_on_submit():
		post.marks=form.grade.data
		db.session.commit()
		flash('Marks Have Been Added Succesfuly', 'success')
		return redirect(url_for('ViewSubmited'))
	return render_template('mark_assignment.html',form=form, post=post)

@app.route("/student_search", methods=['GET', 'POST'])
def student_search():

	form=SearchStudentForm()	
	if form.validate_on_submit():
		marks=SubmittedAssignment.query.filter_by(student_name=form.name.data).all()
		return render_template('result.html', result=marks)