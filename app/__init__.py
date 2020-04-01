from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from datetime import datetime

app = Flask (__name__)

app.config['SECRET_KEY']='5746cb7f101ab30fae9ef946b5bd152eaf79'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app.config['VIDEO_UPLOADS']='app/static/videos'
app.config['NOTES_UPLOAD']='app/static/notes'
app.config['ASSIGNMENTS_UPLOAD']='app/static/assignments'
app.config['ALLOWED_VIDEOS']=[ "MP4",  "GIF","AVI", "WEBM"]
app.config['ALLOWED_DOCS']=[ "DOC",  "DOCX", "PDF","TXT"]

db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)

login_manager.login_view='login'
login_manager.login_message_category='info'

from app import routes