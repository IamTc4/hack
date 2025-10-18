from flask import Blueprint, render_template
from models.event import Fest, Event
from models.winner import Winner
from models.college import Class, Department
from models.tally import Tally
from models.config import SystemConfig

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def home():
    youtube_url_config = SystemConfig.query.filter_by(key='YOUTUBE_LIVE_URL').first()
    countdown_time_config = SystemConfig.query.filter_by(key='COUNTDOWN_TIME').first()

    youtube_url = youtube_url_config.value if youtube_url_config else ''
    countdown_time = countdown_time_config.value if countdown_time_config else ''

    fests = Fest.query.all()

    return render_template('public/home.html', youtube_url=youtube_url, countdown_time=countdown_time, fests=fests)

@public_bp.route('/fests/<int:fest_id>')
def fest_details(fest_id):
    fest = Fest.query.get_or_404(fest_id)
    return render_template('public/fest_details.html', fest=fest)

@public_bp.route('/events/<int:event_id>')
def event_details(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('public/event_details.html', event=event)

@public_bp.route('/leaderboard')
def leaderboard():
    return render_template('public/leaderboard.html')

@public_bp.route('/leaderboard/data')
def leaderboard_data():
    tallies = Tally.query.all()
    department_standings = {}
    for tally in tallies:
        department_name = tally.class_info.department.name
        if department_name not in department_standings:
            department_standings[department_name] = {'gold': 0, 'silver': 0, 'bronze': 0}
        department_standings[department_name]['gold'] += tally.gold
        department_standings[department_name]['silver'] += tally.silver
        department_standings[department_name]['bronze'] += tally.bronze

    # Sort the department standings
    sorted_standings = sorted(department_standings.items(), key=lambda item: (item[1]['gold'], item[1]['silver'], item[1]['bronze']), reverse=True)

    categories = [item[0] for item in sorted_standings]
    gold_data = [item[1]['gold'] for item in sorted_standings]
    silver_data = [item[1]['silver'] for item in sorted_standings]
    bronze_data = [item[1]['bronze'] for item in sorted_standings]

    series = [
        {'name': 'Gold', 'data': gold_data, 'color': '#FFD700'},
        {'name': 'Silver', 'data': silver_data, 'color': '#C0C0C0'},
        {'name': 'Bronze', 'data': bronze_data, 'color': '#CD7F32'}
    ]

    # Mock Hall of Fame data
    hall_of_fame = [
        {'name': 'John Doe', 'event': 'Robo Wars', 'year': 2022},
        {'name': 'Jane Smith', 'event': 'Lazer Tag', 'year': 2022},
        {'name': 'Peter Jones', 'event': 'Xavier Challenge Track', 'year': 2022},
    ]

    return jsonify({'categories': categories, 'series': series, 'hall_of_fame': hall_of_fame})