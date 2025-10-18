from . import db

class Tally(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    gold = db.Column(db.Integer, default=0)
    silver = db.Column(db.Integer, default=0)
    bronze = db.Column(db.Integer, default=0)

    # Establish a relationship to the Class model
    class_info = db.relationship('Class', backref='tally', uselist=False)
