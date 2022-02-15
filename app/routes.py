from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, login_required
from app.models import User
from flask_login import logout_user
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm, EditProfileForm, EditPlantForm
from app.models import Plant
from datetime import datetime


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    plant_form = EditPlantForm()
    if plant_form.validate_on_submit():
        plant = Plant(plant_name=plant_form.plant_name.data, owner=current_user)
        db.session.add(plant)
        db.session.commit()
        flash('New plant is registered!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    plants = current_user.owned_plants().paginate(page, app.config['PLANTS_PER_PAGE'], False)
    next_url = url_for('index', page=plants.next_num) if plants.has_next else None
    prev_url = url_for('index', page=plants.prev_num) if plants.has_prev else None

    return render_template("index.html", title='Home Page', form=plant_form, plants=plants.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/plant/<plant_id>')
@login_required
def plant_page(plant_id):
    plant = Plant.query.filter_by(id=plant_id).first_or_404()
    return render_template('plant_details.html', plant=plant)


@app.route('/plant/<plant_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_plant(plant_id):
    form = EditPlantForm()
    if form.validate_on_submit():
        plant = Plant.query.filter_by(id=plant_id).first()
        plant.plant_name = form.plant_name.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_plant', plant_id=plant_id))
    elif request.method == 'GET':
        plant = Plant.query.filter_by(id=plant_id).first()
        form.plant_name.data = plant.plant_name
    return render_template('edit_plant.html', title='Edit Plant', form=form)