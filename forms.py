from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, RadioField
from wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm):
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=45)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=80)])
	submit = SubmitField('submit')
		
class RegisterForm(FlaskForm):
	email = StringField('email', validators=[InputRequired(), Email(message='Invalid Email'), Length(min=4, max=45)])
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=80)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=80)])
	submit = SubmitField('submit')
	
class InfoForm(FlaskForm):
	name = StringField('name', validators=[InputRequired(), Length(min=5, max=80)])
	content = TextAreaField('content', validators=[InputRequired()])
	submit = SubmitField('submit')

class EventForm(FlaskForm):
	indexName = StringField('name', validators=[InputRequired()])
	indexContent = TextAreaField('content', validators=[InputRequired()])
	summerName = StringField('name', validators=[InputRequired()])
	summerContent = TextAreaField('content', validators=[InputRequired()])
	submit = SubmitField('submit')
	
class FileForm(FlaskForm):
	file = FileField('file', validators=[InputRequired()])
	submit = SubmitField()
	
class AddSet(FlaskForm):
	set = StringField('set', validators=[InputRequired()])
	submit = SubmitField()