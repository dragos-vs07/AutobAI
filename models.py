from datetime import datetime
from extensions import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(80) , unique = True , nullable = False)
    email =  db.Column(db.String(80) , unique = True , nullable = False)
    password_hash = db.Column(db.String(255) ,  nullable = False)
    creation_date = db.Column(db.DateTime , default = datetime.utcnow)
    listings = db.relationship('Listing' , backref = 'seller', lazy = True)

class CarMake(db.Model):
    __tablename__ = 'car_make'
    id = db.Column(db.Integer,primary_key = True)
    brand = db.Column(db.String(80) , unique = True , nullable = False)
    
    models = db.relationship('CarModel' , backref = 'make' , lazy = True)

class CarModel(db.Model):
     __tablename__ = 'car_model'
     id = db.Column(db.Integer,primary_key = True)
     make_id = db.Column(db.Integer , db.ForeignKey('car_make.id'), nullable = False)
     model = db.Column(db.String(80) ,  nullable = False)

class Listing(db.Model):
    __tablename__ = 'listing'
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    make_id = db.Column(db.Integer, db.ForeignKey('car_make.id'), nullable = False)
    model_id = db.Column(db.Integer, db.ForeignKey('car_model.id'), nullable = False)

    title = db.Column(db.String(120), nullable = False)
    price_usd = db.Column(db.Integer, nullable = False)

    drivetrain = db.Column(db.String(40) , nullable = True)
    fuel_type = db.Column(db.String(40) , nullable = True)
    transmission = db.Column(db.String(40) , nullable = True)
    description = db.Column(db.Text, nullable = True)
    fabrication_year = db.Column(db.Integer, nullable = True)
    mileage = db.Column(db.Integer , nullable = True)
    horsepower = db.Column(db.Integer, nullable = True)
    engine_displacement = db.Column(db.Integer, nullable = True)
    fuel_ef = db.Column(db.Float, nullable = True)
    colour = db.Column(db.String(40), nullable = True)
    body_style = db.Column(db.String(40), nullable = True)

    # these are NULL unless the car is sold thus also signaling the selling happened and the car is no longer on listing
    sell_date = db.Column(db.DateTime , nullable = True) 
    sell_price = db.Column(db.Integer , nullable = True)

    status = db.Column(db.String(20), default='private', index=True ) # seller can make the listing private or public 
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    images = db.relationship('ListingImages', backref = 'listing', lazy=True, cascade='all, delete-orphan')

class ListingImages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer , db.ForeignKey('listing.id') , nullable = False)
    image_path = db.Column(db.String(255) , nullable = False)
    cover_image = db.Column(db.Boolean , nullable = False)

class Conversations(db.Model):
    __tablename__ = 'conversation'
    id = db.Column(db.Integer, primary_key=True)
    user_id_1 = db.Column(db.Integer, db.ForeignKey('user.id') , nullable = False)
    user_id_2 = db.Column(db.Integer, db.ForeignKey('user.id') , nullable = False)
    messages = db.relationship('Messages', backref='conversation', lazy=True)

class Messages(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer , db.ForeignKey('conversation.id') , nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id') , nullable = False)
    content = db.Column(db.Text , nullable = False)
    send_date = db.Column(db.DateTime, default=datetime.utcnow)
