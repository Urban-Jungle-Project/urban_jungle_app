from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm, EditPlantForm
from app.models import User, Plant
from app.main import bp


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    plant_form = EditPlantForm()
    if plant_form.validate_on_submit():
        plant = Plant(plant_name=plant_form.plant_name.data, owner=current_user)
        db.session.add(plant)
        db.session.commit()
        flash('New plant is registered!')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    plants = current_user.owned_plants().paginate(page, current_app.config['PLANTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=plants.next_num) if plants.has_next else None
    prev_url = url_for('main.index', page=plants.prev_num) if plants.has_prev else None

    return render_template("index.html", title='Home Page', form=plant_form, plants=plants.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/plant/<plant_id>')
@login_required
def plant_page(plant_id):
    plant = Plant.query.filter_by(id=plant_id).first_or_404()
    return render_template('plant_details.html', plant=plant)


@bp.route('/plant/<plant_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_plant(plant_id):
    form = EditPlantForm()
    if form.validate_on_submit():
        plant = Plant.query.filter_by(id=plant_id).first()
        plant.plant_name = form.plant_name.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_plant', plant_id=plant_id))
    elif request.method == 'GET':
        plant = Plant.query.filter_by(id=plant_id).first()
        form.plant_name.data = plant.plant_name
    return render_template('edit_plant.html', title='Edit Plant', form=form)