import os
from app import app
from flask import request, render_template, flash, redirect
def upload_file():
	if request.method=='POST':
		if request.files:
			fle=request.files["file"]
			if not allowed_extensions(fle.filename):
				flash('File Extension Not Allowed', 'danger')
				return redirect(request.url)
			fle.save(os.path.join(app.config['VIDEO_UPLOADS'], fle.filename))
			flash("file saved", 'success')
			return redirect(request.url)
	return render_template('upload_file.html')

def allowed_extensions(file_name):
	if not "." in file_name:
		return False
	_=file_name.rsplit(".", 1)[1]
	if _.upper() in app.config['ALLOWED_EXTENSIONS']:
		return True
	else:
		return False
