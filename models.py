from config import db, app
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(50))
	username = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(80))
	
class Info(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column('name', db.String(90))
	content = db.Column('content', db.Text())
	
class Set(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column('name', db.String(100), unique=True)
	tag = db.Column('tag', db.String(100))
	images = db.relationship('Images', backref="set", passive_deletes=True, lazy="dynamic")
	
class Images(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column('name', db.String(100))
	set_id = db.Column(db.Integer, db.ForeignKey('set.id', ondelete='CASCADE'))
	
	
class Notice(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	created_at = db.Column('created_at', db.DateTime(timezone=True), default=datetime.now(), nullable=True)
	name = db.Column('name', db.String(90))
	content = db.Column('content', db.Text())

class MeetingDate(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	created_at = db.Column('created_at', db.DateTime(timezone=True), default=datetime.now(), nullable=True)
	name = db.Column('name', db.String(90))
	content = db.Column('content', db.Text())

class ClubMembers(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	created_at = db.Column('created_at', db.DateTime(timezone=True), default=datetime.now(), nullable=True)
	name = db.Column('name', db.String(90))
	content = db.Column('content', db.Text())

class Contact(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	created_at = db.Column('created_at', db.DateTime(timezone=True), default=datetime.now(), nullable=True)
	name = db.Column('name', db.String(90))
	content = db.Column('content', db.Text())

class Events(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	event = db.Column(db.String(95))
	date = db.Column(db.DateTime())

class HomePageSchedule(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column('name', db.String(90))
	content = db.Column('content', db.Text())

class SummerPageSchedule(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column('name', db.String(90))
	content = db.Column('content', db.Text())

	