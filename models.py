from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Apartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    area = db.Column(db.Float, nullable=False)
    region = db.Column(db.String(100), nullable=False)
    block = db.Column(db.String(50), nullable=True)
    building = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    categories = db.Column(db.PickleType, nullable=False)
    images = db.Column(db.PickleType, nullable=True) 