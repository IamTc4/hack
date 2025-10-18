from models import db
from models.event import Event
from datetime import datetime, timedelta

def automate_content_lifecycle():
    """
    Automates the content lifecycle by archiving old events and updating event statuses.
    """
    three_days_ago = datetime.now() - timedelta(days=3)
    thirty_days_ago = datetime.now() - timedelta(days=30)

    # Move events from "Upcoming" to "Results"
    upcoming_events = Event.query.filter(Event.status == 'upcoming', Event.date < three_days_ago).all()
    for event in upcoming_events:
        event.status = 'results'

    # Archive old events
    old_events = Event.query.filter(Event.status == 'results', Event.date < thirty_days_ago).all()
    for event in old_events:
        event.status = 'archived'

    db.session.commit()
