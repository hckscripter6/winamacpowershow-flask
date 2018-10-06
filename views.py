from config import app, db
from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm, RegisterForm, InfoForm, FileForm, AddSet, EventForm
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Info, Images, Set, Notice, MeetingDate, ClubMembers, HomePageSchedule, SummerPageSchedule
import boto3

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#turns string into slug
def tag_generator(val):
	a = val.split()
	b = "-".join(a)
	c = b.lower()
	d = c.strip()
	e = d.replace(",", "")
	f = e.replace(".", "")
	g = f.replace("!", "")
	return g

s3 = boto3.resource('s3')
bucket = s3.Bucket('winamacpowershow-app')
s3projects = "https://d4s3hk8ew6h0g.cloudfront.net/Tractor Show"

@login_manager.user_loader
def load_user(user_id):	
	return User.query.get(int(user_id))
	
@app.route('/', methods=["GET", "POST"])
def index():
	notification = Notice.query.order_by(Notice.created_at.desc()).all()
	events = HomePageSchedule.query.first()
	return render_template('index.html', notification=notification, events = events)
	
'''@app.route('/signup', methods=["GET", "POST"])
def signup():
	form = RegisterForm()
	if form.validate_on_submit():
		hashed_password = generate_password_hash(form.password.data, method='sha256')
		new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(new_user)
		db.session.commit()
		return '<h1>New user has been created</h1>'
	return render_template('authentication/signup.html', form=form)'''
	
@app.route('/login', methods=["GET", "POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user:
			if check_password_hash(user.password, form.password.data):
				login_user(user)
				return redirect(url_for('dashboard'))
	return render_template('authentication/login.html', form=form)
	
@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
#access info data
	info = Info.query.all()
	notifications = Notice.query.order_by(Notice.created_at.desc()).all()
	return render_template('authentication/dashboard.html', info=info, notifications=notifications)
	
@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))
	
@app.route('/dashboard/create', methods=['GET', 'POST'])
@login_required
def create():
	form = InfoForm()
	if form.validate_on_submit():
		create = Info(name=request.form["name"], content=request.form["content"])
		db.session.add(create)
		db.session.commit()
		return redirect(url_for('dashboard'))
	return render_template('authentication/create.html', form=form)
	
@app.route('/dashboard/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
	form = InfoForm()
	info = Info.query.filter_by(id=id).first()
	form.name.data = info.name
	form.content.data = info.content
	
	if form.validate_on_submit():
		info.name = request.form['name']
		info.content = request.form['content']
		db.session.commit()
		return redirect(url_for('dashboard'))
	return render_template('authentication/update.html', form=form, info=info)
	
@app.route('/dashboard/notification/create', methods=['GET', 'POST'])
@login_required
def create_notification():
	form = InfoForm()
	if form.validate_on_submit():
		create = Notice(name=form.name.data, content=form.content.data)
		db.session.add(create)
		db.session.commit()
		return redirect(url_for('dashboard'))
	return render_template('authentication/create_notification.html', form=form)
	
@app.route('/dashboard/notification/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_notification(id):
	form = InfoForm()
	notification = Notice.query.filter_by(id=id).first()
	form.name.data = notification.name
	form.content.data = notification.content
	
	if form.validate_on_submit():
		notification.name = request.form['name']
		notification.content = request.form['content']
		db.session.commit()
		return redirect(url_for('dashboard'))
	return render_template('authentication/update_notification.html', form=form, notification=notification)

@app.route('/dashboard/notification/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_notification(id):
	notification = Notice.query.filter_by(id=id).first()
	db.session.delete(notification)
	db.session.commit()
	return redirect(url_for("dashboard"))

@app.route('/dashboard/event-schedule/edit', methods=['GET', 'POST'])
@login_required
def update_event_schedule():
	form = EventForm()
	summerEventQuery = SummerPageSchedule.query.first()
	indexEventQuery = HomePageSchedule.query.first()

	form.indexName.data = indexEventQuery.name
	form.indexContent.data = indexEventQuery.content

	form.summerName.data = summerEventQuery.name
	form.summerContent.data = summerEventQuery.content

	if form.validate_on_submit():
		indexEventQuery.name = request.form["indexName"]
		indexEventQuery.content = request.form["indexContent"]

		summerEventQuery.name = request.form["summerName"]
		summerEventQuery.content = request.form["summerContent"]


		db.session.commit()
		redirect(url_for('update_event_schedule'))
		
	return render_template('authentication/event-schedule.html', form=form)

'''	
@app.route('/dashboard/notification/create', methods=['GET', 'POST'])
@login_required
def create_notification():
	form = InfoForm()
	if form.validate_on_submit():
		create = Notice(name=form.name.data, content=form.content.data)
		db.session.add(create)
		db.session.commit()
		return redirect(url_for('dashboard'))
	return render_template('authentication/create_notification.html', form=form)
'''
@app.route('/dashboard/meeting-date/update', methods=['GET', 'POST'])
@login_required
def update_meeting_date():
	form = InfoForm()
	dates = MeetingDate.query.first()
	form.name.data = dates.name
	form.content.data = dates.content

	if form.validate_on_submit():
		dates.name = request.form['name']
		dates.content = request.form['content']
		db.session.commit()
		return redirect(url_for('dashboard'))
	return render_template('authentication/update_meeting_date.html', form=form, dates=dates)

@app.route('/dashboard/club-members/update', methods=['GET', 'POST'])
@login_required
def update_club_members():
	form = InfoForm()
	members = ClubMembers.query.first()
	dates = MeetingDates.query.first()
	form.name.data = members.name
	form.content.data = members.content

	if form.validate_on_submit():
		members.name = request.form['name']
		members.content = request.form['content']
		db.session.commit()
		return redirect(url_for('dashboard'))
	return render_template('authentication/update_meeting_date.html', form=form, members=members, dates=dates)

@app.route('/dashboard/photos', methods=['GET', 'POST'])
@login_required
def edit_photos():
	upload = FileForm()
	set_loop =  Set.query.order_by(Set.id.desc()).all()
	if upload.validate_on_submit():
		for loop in set_loop:
			if request.form["select_set"] == loop.tag:
				file = request.files['file']
				bucket.put_object(Key='Tractor Show/'+ loop.name + '/' + file.filename, Body=file)
				newFile = Images(name=file.filename, set=loop)
				db.session.add(newFile)
				db.session.commit()	
				return redirect('/dashboard/photos#'+loop.tag)

	add_set = AddSet()
	if add_set.validate_on_submit():
		render_tag = tag_generator(request.form["set"])
		new_set = Set(name=request.form["set"], tag=render_tag)
		db.session.add(new_set)
		db.session.commit()
		return redirect(url_for('edit_photos'))
	return render_template('authentication/edit-photos.html', upload=upload, add_set=add_set, set_loop=set_loop, s3projects=s3projects)

@app.route('/dashboard/photos/<set>/<image>', methods=['GET', 'POST'])
@login_required
def single_photo(set, image):
	single = Images.query.filter_by(name=image).first()
	return render_template('authentication/single_image.html', single=single, s3projects=s3projects)

@app.route('/dashboard/photos/<set>/<image>/delete')
@login_required
def delete_photo(set, image):
	single = Images.query.filter_by(name=image).first()
	db.session.delete(single)
	db.session.commit()
	return render_template('authentication/photo-deleted.html')


@app.route('/dashboard/photos/set/<set>', methods=['GET', 'POST'])
@login_required
def delete_set(set):
	destroy_set = Set.query.filter_by(tag=set).first()
	db.session.delete(destroy_set)
	db.session.commit()
	return 'set deleted'
	
@app.route('/events/summer-show', methods=['GET', 'POST'])
def summer_show():
	info = Info.query.filter_by(name="Summer Show Info").first()
	events = SummerPageSchedule.query.first()
	return render_template('summer_show.html', info=info, events=events)
	
@app.route('/events/toy-show', methods=['GET', 'POST'])
def toy_show():
	return render_template('toy_show.html')
	
	
@app.route('/information/exhibitor-info', methods=['GET', 'POST']) 
def exhibitor_info():
	info = Info.query.filter_by(name='Exhibitor Information').first()
	return render_template('exhibitor_info.html', info=info)

@app.route('/information/exhibitor-camping', methods=['GET', 'POST']) 
def exhibitor_camping():
	info = Info.query.filter_by(name='Camping for Exhibitors').first()
	return render_template('exhibitor_camping.html', info=info)
	
@app.route('/information/food-vendor', methods=['GET', 'POST']) 
def food_vendor():
	info = Info.query.filter_by(name='Food Vendor Information').first()
	return render_template('food_vendor.html', info=info)
	
@app.route('/information/flea-market', methods=['GET', 'POST']) 
def flea_market():
	info = Info.query.filter_by(name='Flea Market Vendor Info').first()
	return render_template('flea_market.html', info=info)	

@app.route('/information/toy-show', methods=['GET', 'POST']) 
def toy_vendor():
	info = Info.query.filter_by(name='Toy Vendor Info').first()
	return render_template('toy_vendor.html', info=info)	
	
@app.route('/information/golf_cart_policy', methods=['GET', 'POST']) 
def golf_cart():
	info = Info.query.filter_by(name='Golf Cart Policy').first()
	return render_template('golf_cart.html', info=info)	
	
@app.route('/contact', methods=['GET', 'POST']) 
def contact():
	return render_template('contact.html')	
	
@app.route('/information/directions', methods=['GET', 'POST']) 
def directions():
	return render_template('directions.html')

@app.route('/information/club_info', methods=['GET', 'POST']) 
def club_info():
	members = ClubMembers.query.first()
	dates = MeetingDate.query.first()
	return render_template('club_info.html', members=members, dates=dates)	

@app.route('/information/scholarship', methods=['GET', 'POST']) 
def scholarship():
	info = Info.query.filter_by(name="Northern Indiana Power from the Past Scholarships").first()
	return render_template('scholarship.html', info=info)	

@app.route('/photos', methods=['GET', 'POST'])
def photos():
	sets = Set.query.order_by(Set.id.desc()).join(Images).all()
	return render_template('photos.html', sets=sets, s3projects=s3projects)
