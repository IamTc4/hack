from models import db
from models.college import Class
from models.tally import Tally

def update_tally(class_id, medal):
    tally = Tally.query.filter_by(class_id=class_id).first()
    if not tally:
        tally = Tally(class_id=class_id)
        db.session.add(tally)

    if medal == 'Gold':
        tally.gold += 1
    elif medal == 'Silver':
        tally.silver += 1
    elif medal == 'Bronze':
        tally.bronze += 1
    db.session.commit()
