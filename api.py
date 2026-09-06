from flask import Blueprint, request, session, jsonify
from extensions import db
from models import CarMake, CarModel, Listing, Favorites, User

api = Blueprint("api", __name__, url_prefix="/API")


@api.route("/get_models/<string:brand>")
def find_models(brand):
    b = CarMake.query.filter_by(brand=brand).first()

    return jsonify([
        {
            "id": model.id,
            "model": model.model
        }
        for model in b.models
    ])


# 24 listings on one page
# IMPLEMENT FILTERS
@api.route("/check_favourite")
def check_fav():
    listing_id = request.args.get("listing_id",-1,type=int)
    listing = Listing.query.filter_by(id=listing_id).first()

    if not listing or not session.get("user_id") or session.get("user_id") == listing.seller_id:
        return jsonify({
            "status": "fail"
        })

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
                "status": "success",
                "favourited": "False" if row else "True"
            })

@api.route("/get_listings")
def find_listings():

    page = request.args.get("page", 1, type=int)
    seller_id = request.args.get("seller_id", -1, type=int)
    listings_per_page = min(request.args.get("lpp", 1, type=int), 50)
    favourites = request.args.get("favourites",False,type=bool)

    listings = []

    if seller_id != -1 and (not session.get("user_id") or session.get("user_id") != seller_id): # get all listings of a user different from the one logged in 
        listings = Listing.query.filter_by(seller_id=seller_id, status="public").offset(        # ( only public ones )
            (page - 1) * listings_per_page).limit(listings_per_page).all()

    elif seller_id != -1 and session.get("user_id") == seller_id: # get all listings of current logged in user
        if not favourites:
            listings = Listing.query.filter_by(seller_id=seller_id).offset(
                        (page - 1) * listings_per_page).limit(listings_per_page).all()
        else:
            seller = User.query.filter_by(id=session.get("user_id")).first()
            listings = [ Listing.query.get(fav.listing_id) for fav in seller.favorites]
    else:
        listings = Listing.query.filter_by(status="public").offset( # get all listings on the website
            (page - 1) * listings_per_page).limit(listings_per_page).all()

    return jsonify([{
        "listing_id": l.id,
        "seller_id": l.seller_id,
        "title": l.title,
        "price": l.price,
        "brand": l.other_make if l.other_make else CarMake.query.filter_by(id=l.make_id).first().brand,
        "model": l.other_model if l.other_model else CarModel.query.filter_by(id=l.model_id).first().model,
        "mileage": l.mileage,
        "cover_img_path": l.images.filter_by(cover_image=True).first().image_path,
        "views": l.views,
        "favorites": len(Favorites.query.filter_by(listing_id=l.id).all()),
        "is_favourite": "True" if session.get("user_id") and Favorites.query.filter_by(listing_id=l.id, user_id=session.get("user_id")).first() else "False"
    } for l in listings])

