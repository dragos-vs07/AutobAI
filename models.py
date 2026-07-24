from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(80) , unique = True , nullable = False)
    email =  db.Column(db.String(80) , unique = True , nullable = False)
    password_hash = db.Column(db.String(255) ,  nullable = False)
    creation_date = db.Column(db.DateTime , default = datetime.utcnow)

class CarMake(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    brand = db.Column(db.String(80) , unique = True , nullable = False)

class CarModel(db.Model):
     id = db.Column(db.Integer,primary_key = True)
     model = db.Column(db.String(80) , unique = True , nullable = False)

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    make_id = db.Column(db.Integer, db.ForeignKey('car_make.id'), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('car_model.id'), nullable=False)

    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)

    price_eur = db.Column(db.Integer, nullable=False)
    fabrication_year = db.Column(db.Integer, nullable=False)
    horsepower = db.Column(db.Integer, nullable=True)
    engine_displacement = db.Column(db.Integer, nullable=True)
    consumption = db.Column(db.Integer, nullable=True)
    colour = db.Column(db.String(40), nullable=True)
    body_style = db.Column(db.String(40), nullable=True)
    had_accident = db.Column(db.Boolean, default=False)

    status = db.Column(db.String(20), default='active')
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
