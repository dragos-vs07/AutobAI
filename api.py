from models import CarMake, CarModel, Listing, Favorites, User
from flask import Blueprint, request, session, jsonify
from extensions import db
import os
import json 
import pandas as pd
import lightgbm as lgbm
from datetime import datetime
from constants import body_styles, engine_configurations, fuel_types, drivetrains, transmissions, countries

api = Blueprint("api", __name__, url_prefix="/API")

MODEL_PATH = os.path.join(os.path.dirname(__file__), "ml", "autobay_price_model.txt")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "ml", "categories.json")

price_model = lgbm.Booster(model_file = MODEL_PATH)

with open(CATEGORIES_PATH) as f:
    categories = json.load(f)

from pandas.api.types import CategoricalDtype

@api.route("/predict_price")
def make_prediction():

    user_inputs = ["make","model","fuel_type","transmission","mileage","year","power","offer"]
    user_data = []

    listing_id = request.args.get("listing_id",None)

    if listing_id:  # prediction is made for a chosen listing from the database
        l = Listing.query.filter_by(id = listing_id).first()
        if not l:
            return jsonify({
                "message" : "Listing not found"
            }), 404

        # listing must either pe public or the user_id and seller_id must coincide
        if l.status == "private" and session.get("user_id") != l.seller_id:
            return jsonify({
                "message" : "Evaluation not authorised"
            }), 403



        user_data.append(CarMake.query.filter_by(id = l.make_id).first().brand if l.make_id else l.other_make)
        user_data.append(CarModel.query.filter_by(id = l.model_id).first().model if l.model_id else l.other_model) 
        user_data.append(l.fuel_type)
        user_data.append(l.transmission)
        user_data.append(l.mileage)
        user_data.append(l.year)
        user_data.append(l.power)

        if l.mileage is None or ( l.mileage and l.mileage > 5000 ):
            user_data.append("Used")
        else:
            user_data.append("New") 

    else:  
        for f in user_inputs:
            user_data.append(request.args.get(f, None))

    if user_data[2] == "Other":
        user_data[2] = "Others"

    if user_data[3] == "Semi-Automatic":
        user_data[3] = "Semi-automatic";
    
    if user_data[5]:
        user_data[5] = datetime.now().year - int(user_data[5])

    input_row = {}

    features = ["make","model","fuel","gear","mileage","age","hp","offerType"]

    for i, f in enumerate(features):
        if i != 4 and i != 5 and i != 6:
            input_row[f] = user_data[i] if user_data[i] and user_data[i] != "Unknown" else None
        else:
            input_row[f] = float(user_data[i]) if user_data[i] else None

    X = pd.DataFrame([input_row], columns=features)

    cat_features = ["make", "model", "fuel", "gear", "offerType"]
    num_features = ["mileage","age","hp"]

    for f in cat_features:
        X[f] = X[f].astype(CategoricalDtype(categories=categories[f]))

    for f in num_features:
        X[f] = X[f].astype("float64")
        
    prediction = price_model.predict(X)

    return jsonify({
        "predicted_price": int(prediction[0])
    }), 200

@api.route("/get_models/<string:brand>")
def find_models(brand):
    b = CarMake.query.filter_by(brand=brand).first()

    if not b:
        return jsonify([{
            "message": "No such brand found"
        }]), 404;
    
    model_list = b.models
    
    return jsonify([
        {
            "id": model.id,
            "model": model.model
        }
        for model in b.models
    ]), 200


@api.route("/toggle_favourite", methods = ["POST"])
def toggle_fav():

    if not session.get("user_id"):
        return jsonify({
                    "message": "not authenticated"
                }), 401
    
    listing_id = request.args.get("listing_id",-1,type=int)

    if listing_id == -1:
        return jsonify({
            "message": "no listing id provided"
        }), 400
    
    listing = Listing.query.filter_by(id=listing_id).first()

    if not listing:
        return jsonify({
            "message": "listing not found"
        }), 404
    
    if  session.get("user_id") == listing.seller_id:
        return jsonify({
            "message": "user not authorised for this listing"
        }), 403

    row = Favorites.query.filter_by(listing_id=listing_id, user_id=session.get("user_id")).first()

    if row:
        db.session.delete(row)
    else:
        db.session.add(Favorites(
            user_id = session.get("user_id"),
            listing_id = listing_id
        ))

    db.session.commit()

    return jsonify({
                "favourited": not bool(row)
            }), 200

NUMERIC_COLUMNS = {
    "power": "power", "year": "year", "price": "price",
    "displacement": "displacement", "mileage": "mileage",
    "fuel_ef": "fuel_efficiency",
}

CATEGORICAL_COLUMNS = {
    "body_style": "body_style",
    "fuel_type": "fuel_type",
    "engine_config": "configuration",
    "transmission": "transmission",
    "drivetrain": "drivetrain",
    "country" : "country"
}

KNOWN_VALUES = {
    "body_style":    body_styles,             # use the same lists your template gets
    "fuel_type":     fuel_types,
    "engine_config": engine_configurations,
    "transmission":  transmissions,
    "drivetrain":    drivetrains,
    "country": countries 
}

SORT_OPTIONS = {
    "newest":       Listing.id.desc(),
    "price_asc":    Listing.price.asc(),
    "price_desc":   Listing.price.desc(),
    "mileage_asc":  Listing.mileage.asc(),
    "mileage_desc": Listing.mileage.desc(),
    "year_desc":    Listing.year.desc(),
    "year_asc":     Listing.year.asc(),
}

def in_or_other(col, values, other_cond):
    known = [v for v in values if v != "Other"]
    conds = []
    if known:
        conds.append(col.in_(known))      # the checked fixed options
    if "Other" in values:
        conds.append(other_cond)          # the "Other" condition passed in
    return db.or_(*conds)

@api.route("/get_listings")
def find_listings():
    page = max(1, request.args.get("page", 1, type=int))
    seller_id = request.args.get("seller_id", -1, type=int)
    listings_per_page = max(1, min(request.args.get("lpp", 24, type=int), 50))
    favourites = request.args.get("favourites")
    user_search_input = request.args.get("ui", '').strip()
    current_user_id = session.get("user_id")

    if favourites:
        favourites = favourites.lower() == "true"

    listings = (Listing.query
                .outerjoin(CarMake, Listing.make_id == CarMake.id)
                .outerjoin(CarModel, Listing.model_id == CarModel.id))

    
    if current_user_id != seller_id:
        listings = listings.filter(Listing.status == "public")  # all listings for a user getting his own listings, just public otherwise

    if seller_id != -1:
        if not User.query.filter_by(id = seller_id).first():
            return None, None, None, "User not found"
        
        listings = listings.filter(Listing.seller_id == seller_id) # if a certain seller's listings are sought

    if favourites:  # if favourites are sought
        if not current_user_id:    # if the user isnt logged in we just return empty
            return jsonify({"total": 0, "listings": []}), 200
        listings = (listings
                    .join(Favorites, Favorites.listing_id == Listing.id)
                    .filter(Favorites.user_id == current_user_id))

    # keyword search 
    for t in user_search_input.split():
        if t.isdigit() and len(t) == 4:
            listings = listings.filter(Listing.year == int(t))
        else:
            listings = listings.filter(db.or_(
                Listing.title.ilike(f'%{t}%'),
                CarMake.brand.ilike(f'%{t}%'),
                CarModel.model.ilike(f'%{t}%'),
                Listing.other_make.ilike(f'%{t}%'),
                Listing.other_model.ilike(f'%{t}%'),
            ))

    makes = request.args.getlist("make")
    
    if makes:
        other_make_cond = db.or_(
        Listing.make_id.is_(None),
        CarMake.brand == "Unknown",
        db.and_(Listing.other_make.isnot(None), Listing.other_make != ""),
    )
        listings = listings.filter(in_or_other(CarMake.brand, makes, other_make_cond))

    models = request.args.getlist("model")
    if models:
        other_model_cond = db.or_(
        Listing.model_id.is_(None),
        CarModel.model == "Unknown",
        db.and_(Listing.other_model.isnot(None), Listing.other_model != ""),
    )
        listings = listings.filter(in_or_other(CarModel.model, models, other_model_cond))

    for param, column in CATEGORICAL_COLUMNS.items():
        values = request.args.getlist(param)
        if values:
            col = getattr(Listing, column)
            other_cond = db.or_(
                col.is_(None),
                col == "",
                col == "Unknown",                 
                col.notin_(KNOWN_VALUES[param]),  # custom text typed by the seller
            )
            listings = listings.filter(in_or_other(col, values, other_cond))

    for param, column in NUMERIC_COLUMNS.items():
        lo = request.args.get(f"min_{param}", type=float)
        hi = request.args.get(f"max_{param}", type=float)
        col = getattr(Listing, column)
        if lo is not None:
            listings = listings.filter(db.or_(col >= lo, col.is_(None)))
        if hi is not None:
            listings = listings.filter(db.or_(col <= hi, col.is_(None)))

    order = SORT_OPTIONS.get(request.args.get("sort", "newest"), SORT_OPTIONS["newest"])

    total = listings.count()

    listings = (listings.order_by(order, Listing.id.desc())
                        .offset((page - 1) * listings_per_page)
                        .limit(listings_per_page)
                        .all())

    return jsonify({
    "total": total,
    "listings": [{
        "listing_id": l.id,
        "seller_id": l.seller_id,
        "seller_name": l.seller.username,
        "seller_type": l.seller.type,
        "title": l.title,
        "price": l.price,
        "brand": l.other_make if l.other_make else CarMake.query.filter_by(id=l.make_id).first().brand,
        "model": l.other_model if l.other_model else CarModel.query.filter_by(id=l.model_id).first().model,
        "mileage": l.mileage,
        "country": l.country,
        "city": l.city,
        "cover_img_path": l.images.filter_by(cover_image=True).first().image_path,
        "views": l.views,
        "favorites": Favorites.query.filter_by(listing_id=l.id).count(),
        "is_favourite": "True" if session.get("user_id") and Favorites.query.filter_by(listing_id=l.id, user_id=session.get("user_id")).first() else "False"
    } for l in listings]
}), 200


@api.route("/delete_listing/<int:listing_id>", methods=["POST"])
def delete_listing(listing_id):

    if not session.get("user_id"):
          return jsonify({
               "status": "fail",
               "message": "Not authenticated"
          }), 401
     
    l = Listing.query.filter_by(id=listing_id).first()

    if not l:
          return jsonify({
               "status": "fail",
               "message": "Listing not found"
          }), 404

    if l.seller_id != session.get("user_id"):
          return jsonify({
               "status": "fail",
               "message": "Unauthorised access for deleting chosen listing"
          }), 403


    paths = [img.image_path for img in l.images]

    try:
        db.session.delete(l)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"status": "fail", "message": "Could not delete listing"}), 500

    for path in paths:
        try:
            os.remove(path)
        except OSError:
            pass

    return '', 204

