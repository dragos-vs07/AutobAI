from flask import Flask , render_template , session , request , flash , redirect , url_for , jsonify
from extensions import db , migrate
from werkzeug.security import generate_password_hash , check_password_hash
from werkzeug.utils import secure_filename
from api import api
from auth import auth
import os
import requests
import pandas as pd
import uuid

app = Flask(__name__)
app.config.from_object("config.Config")

db.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(api)
app.register_blueprint(auth)

from models import User, CarMake, CarModel, Listing, ListingImages,  Conversations, Messages, Favorites

body_styles = [
    "Sedan",
    "Hatchback",
    "Coupe",
    "Convertible",
    "Roadster",
    "Station Wagon",
    "SUV",
    "Crossover",
    "Pickup Truck",
    "Van",
    "Minivan",
    "Liftback",
    "Fastback",
    "Limousine",
    "Other",
    "Unknown"
]

engine_configurations = [
     "Inline-3 (I3)",
     "Inline-4 (I4)",
     "Inline-5 (I5)",
     "Inline-6 (I6)",
     "V6",
     "V8",
     "V10",
     "V12",
     "Flat-4 (Boxer)",
     "Flat-6 (Boxer)",
     "W12",
     "W16",
     "Rotary",
     "Other",
     "Unknown"
     ]

@app.route("/")
def load_home():
    return render_template("index.html")

@app.route("/genp")
def load_general_page():
      return render_template("general_page.html")

@app.route("/viewlisting")
def load_view_listing_page():
     listing_id = request.args.get("listing_id" , -1 , type=int)
     listing = Listing.query.filter_by(id = listing_id).first()

     if not listing :
          return redirect(url_for("load_general_page"))

     if session.get("user_id") != listing.seller_id:
          listing.views = listing.views + 1
          db.session.commit()
     
     return render_template("view_listing_page.html",
                            listing = listing,
                            cover_img_path = listing.images.filter_by(cover_image = True).first().image_path,
                            images = listing.images.filter_by(cover_image = False).all()
                            )

@app.route("/mklistp")
def load_make_listing_page():
    if not session.get("user_id"):
          return redirect(url_for("load_home"))

    return render_template("make_listing_page.html" ,
                           brands = CarMake.query.order_by(CarMake.brand).all() ,
                           engine_configurations = engine_configurations , 
                           body_styles = body_styles
                        )

@app.route("/mylistingsp")
def load_my_listings_page():
     if not session.get("user_id"):
            return redirect(url_for("load_home"))
     
     return render_template("my_listings_page.html",
                            user_id = session.get("user_id") )

@app.route("/predictp")
def load_predict_page():
    return render_template("predict_page.html")

@app.route("/regp")
def load_register_page():
    return render_template("register_page.html")

@app.route("/loginp")
def load_login_page():
    return render_template("login_page.html")

@app.route("/accountp")
def load_account_page():

    if not session.get("user_id"):
      return redirect(url_for("load_home"))

    user = User.query.filter_by(id = session.get("user_id")).first()

    return render_template("account_page.html", user = user)

@app.route("/infop")
def load_information_page():
          if not session.get("user_id"):
                return redirect(url_for("load_home"))
          
          return render_template("information_page.html")
     
# the unit table follows metric , thus as follows:
#  price = euro, mileage = km, engine power = hp(PS),
#  displacement = L, fuel efficiency = l/100km


def normalise_currency(value, unit):
    value = float(value)

    if unit != "dollar":
        return value

    try:
        response = requests.get(
            "https://open.er-api.com/v6/latest/USD",
            timeout=5
        )

        response.raise_for_status()

        data = response.json()

        if data.get("result") != "success":
            return None

        rate = data["rates"]["EUR"]

        return value * rate

    except (
        requests.RequestException,
        KeyError,
        ValueError,
        TypeError
    ):
        return None
    
def normalise_mileage( value , unit):
     if unit == "mile":
            return 1.6 * float(value)
     return float(value)

def normalise_engine_power(value , unit):
     if unit == "kW":
            return 1.36 * float(value)
     return float(value)

def normalise_displacement(value , unit):
     if unit == "cc":
             return float(value) / 1000
     return float(value)

def normalise_fuel_efficiency(value , unit):
     if unit == "mpg":
            return 235.215 / float(value) 
     return float(value)

def save_listing_image(file,is_cover,listing_id):

      ALLOWED = {".jpg", ".jpeg", ".png", ".webp"}
      filename = secure_filename(file.filename)
      ext = os.path.splitext(filename)[1].strip().lower()

      print("here:" , ext)
      if ext not in ALLOWED:
            flash("Invalid image format")
            return
      
      img_path = f"static/listings_images/{uuid.uuid4()}{ext}"
      file.save(img_path)
     
      new_listing_image = ListingImages(
                 listing_id = listing_id,
                 image_path = img_path,
                 cover_image = is_cover
                )

      db.session.add(new_listing_image)

@app.route("/upload_listing" , methods = ["POST"])
def make_listing():

     if not session.get("user_id"):
          return redirect(url_for("load_home"))
     
     inputs = ["make_id", "model_id", "title", "price", "configuration", "drivetrain", "fuel_type",
                "transmission", "description", "year", "mileage", "power", "displacement", "fuel_efficiency",
                "colour", "body_style", "status"  ]

     other_option ={"make_id": False, "model_id" : False, "fuel_type" : False, "configuration" : False, "drivetrain" : False}

     units = ["priceUnit", "MileageUnit", "enginePowerUnit", "engineDisplacementUnit", "fuelEfficiencyUnit"]

     form_data = []
     form_units = []
     
     for i in inputs:
          
          data = request.form.get(i)

          if not data and not Listing.__table__.columns[i].nullable :
               print("here",data)
               flash(f"must input required fields{Listing.__table__.columns[i]}")
               return(redirect(url_for("load_make_listing_page")))
          
          elif not data and Listing.__table__.columns[i].nullable :
                  form_data.append(None)

          else:
                  if data == "Other":
                       other = request.form.get(f"other_{i}")
                       if not other:
                            flash(f"must input other {i}")
                            return(redirect(url_for("load_make_listing_page")))
                       else:
                              other_option[i] = True
                              form_data.append(other)
                  else:
                        form_data.append(data)
               
      
     for u in units:
            unit = request.form.get(u)
            if not unit:
                  flash("must select a unit for measurable inputs")
                  return redirect(url_for("load_make_listing_page"))
            form_units.append(unit)
          

     cover_image = request.files.get("coverCarImage")
     if not cover_image or not cover_image.filename :
            flash("Must submit a cover image")
            return redirect(url_for("load_make_listing_page"))
     
     currency_convert = normalise_currency(form_data[3], form_units[0])

     if not currency_convert:
          flash("Conversion from USD to EUR failed , try manual conversion or use EUR until problem is fixed")
          return redirect(url_for("load_make_listing_page"))

     if len(form_data[2]) > 80:
          flash("Title too long , please shorten the input")
          return redirect(url_for("load_make_listing_page"))

     if len(form_data[8]) > 1000:
          flash("Description too long, please shorten the input")
          return redirect(url_for("load_make_listing_page"))
     
     new_listing = Listing(
           seller_id = session.get("user_id") ,
           make_id = int(form_data[0]) if form_data[0] and not other_option["make_id"] else None,
           model_id = int(form_data[1]) if form_data[1] and not other_option["model_id"] else None,
           other_make = form_data[0] if other_option["make_id"] else None ,
           other_model = form_data[1] if other_option["model_id"] else None ,
           title = form_data[2] ,
           price = currency_convert,
           configuration = form_data[4] ,
           drivetrain = form_data[5] ,
           fuel_type = form_data[6] ,
           transmission = form_data[7] ,
           description = form_data[8] ,
           year = int(form_data[9]) if form_data[9] else None,
           mileage = normalise_mileage(form_data[10],form_units[1]) if form_data[10] else None,
           power = normalise_engine_power(form_data[11],form_units[2]) if form_data[11] else None,
           displacement = normalise_displacement(form_data[12],form_units[3]) if form_data[12] else None,
           fuel_efficiency = normalise_fuel_efficiency(form_data[13] , form_units[4]) if form_data[13] else None,
           colour = form_data[14] ,
           body_style = form_data[15] ,
           status = form_data[16]
      )

     db.session.add(new_listing)
     db.session.commit()


     save_listing_image(cover_image,True,new_listing.id)

     for image in request.files.getlist("carImages"):
            if image.filename:
             save_listing_image(image,False,new_listing.id)

     db.session.commit()

     flash("Listing uploaded successfuly")
     return redirect(url_for("load_make_listing_page"))


if __name__ == "__main__":
        app.run()