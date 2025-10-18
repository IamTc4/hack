from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.winner import Winner
from models.event import Event
from models.college import Class
from services.medal_service import update_tally

portal_bp = Blueprint('portal', __name__)

@portal_bp.route('/portal/dashboard')
@login_required
def dashboard():
    return render_template('portal/dashboard.html')

@portal_bp.route('/portal/submit_result', methods=['GET', 'POST'])
@login_required
def submit_result():
    events = Event.query.all()
    classes = Class.query.all()
    if request.method == 'POST':
        name = request.form.get('name')
        class_id = request.form.get('class_id')
        event_id = request.form.get('event_id')
        medal = request.form.get('medal')

        # Create the winner
        new_winner = Winner(name=name, class_id=class_id, event_id=event_id, medal=medal, submitted_by=current_user.id)
        db.session.add(new_winner)
        db.session.commit()

        # Update the tally
        update_tally(class_id, medal)

        flash('Result submitted successfully!')
        return redirect(url_for('portal.dashboard'))
    return render_template('portal/submit_result.html', events=events, classes=classes)
