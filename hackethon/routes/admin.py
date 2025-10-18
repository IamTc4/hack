from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from models.user import User
from models.event import Fest, Event
from models.winner import Winner
from models.college import Class
from models.config import SystemConfig
from services.medal_service import update_tally

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.home'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    fest_count = Fest.query.count()
    event_count = Event.query.count()
    winner_count = Winner.query.count()
    return render_template('admin/dashboard.html', fest_count=fest_count, event_count=event_count, winner_count=winner_count)

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        youtube_url = request.form.get('youtube_url')
        config = SystemConfig.query.filter_by(key='YOUTUBE_LIVE_URL').first()
        if not config:
            config = SystemConfig(key='YOUTUBE_LIVE_URL', value=youtube_url)
            db.session.add(config)
        else:
            config.value = youtube_url
        db.session.commit()
        flash('Settings updated successfully!')
        return redirect(url_for('admin.settings'))

    youtube_url_config = SystemConfig.query.filter_by(key='YOUTUBE_LIVE_URL').first()
    youtube_url = youtube_url_config.value if youtube_url_config else ''
    return render_template('admin/settings.html', youtube_url=youtube_url)

# Fest Management
@admin_bp.route('/fests')
@login_required
def list_fests():
    fests = Fest.query.all()
    return render_template('admin/fests.html', fests=fests)

@admin_bp.route('/fests/add', methods=['GET', 'POST'])
@login_required
def add_fest():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        new_fest = Fest(name=name, description=description)
        db.session.add(new_fest)
        db.session.commit()
        return redirect(url_for('admin.list_fests'))
    return render_template('admin/fest_form.html')

@admin_bp.route('/fests/edit/<int:fest_id>', methods=['GET', 'POST'])
@login_required
def edit_fest(fest_id):
    fest = Fest.query.get_or_404(fest_id)
    if request.method == 'POST':
        fest.name = request.form.get('name')
        fest.description = request.form.get('description')
        db.session.commit()
        return redirect(url_for('admin.list_fests'))
    return render_template('admin/fest_form.html', fest=fest)

@admin_bp.route('/fests/delete/<int:fest_id>', methods=['POST'])
@login_required
def delete_fest(fest_id):
    fest = Fest.query.get_or_404(fest_id)
    db.session.delete(fest)
    db.session.commit()
    return redirect(url_for('admin.list_fests'))

# Event Management
@admin_bp.route('/events')
@login_required
def list_events():
    events = Event.query.all()
    return render_template('admin/events.html', events=events)

@admin_bp.route('/events/add', methods=['GET', 'POST'])
@login_required
def add_event():
    fests = Fest.query.all()
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        fest_id = request.form.get('fest_id')
        new_event = Event(name=name, description=description, fest_id=fest_id)
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('admin.list_events'))
    return render_template('admin/event_form.html', fests=fests)

@admin_bp.route('/events/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    fests = Fest.query.all()
    if request.method == 'POST':
        event.name = request.form.get('name')
        event.description = request.form.get('description')
        event.fest_id = request.form.get('fest_id')
        db.session.commit()
        return redirect(url_for('admin.list_events'))
    return render_template('admin/event_form.html', event=event, fests=fests)

@admin_bp.route('/events/delete/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('admin.list_events'))

# Winner Management
@admin_bp.route('/winners')
@login_required
def list_winners():
    winners = Winner.query.all()
    return render_template('admin/winners.html', winners=winners)

@admin_bp.route('/winners/add', methods=['GET', 'POST'])
@login_required
def add_winner():
    events = Event.query.all()
    classes = Class.query.all()
    if request..method == 'POST':
        name = request.form.get('name')
        class_id = request.form.get('class_id')
        event_id = request.form.get('event_id')
        medal = request.form.get('medal')

        # Create the winner
        new_winner = Winner(name=name, class_id=class_id, event_id=event_id, medal=medal)
        db.session.add(new_winner)
        db.session.commit()

        # Update the tally
        update_tally(class_id, medal)

        return redirect(url_for('admin.list_winners'))
    return render_template('admin/winner_form.html', events=events, classes=classes)