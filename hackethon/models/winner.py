from . import db

class Winner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    medal = db.Column(db.String(50), nullable=False)  # Gold, Silver, Bronze

    # Define the relationship to the Class model
    class_info = db.relationship('Class', backref=db.backref('winners', lazy=True))
