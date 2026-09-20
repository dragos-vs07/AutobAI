from flask import Flask , render_template , session , request , flash , redirect , url_for 
from extensions import db , migrate
from api import api
from auth import auth
import requests
import uuid
import math
import os
from datetime import datetime
from constants import body_styles, engine_configurations, fuel_types, drivetrains, transmissions

app = Flask(__name__)
app.config.from_object("config.Config")
app.config["MAX_CONTENT_LENGTH"] = 60 * 1024 * 1024

db.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(api)
app.register_blueprint(auth)

from models import User, CarMake, CarModel, Listing, ListingImages,  Conversations, Messages, Favorites

ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp", ".jfif"}

@app.route("/")
def load_home():
    return render_template("index.html")

@app.route("/genp")
def load_general_page():
      return render_template("general_page.html",
               brands = CarMake.query.order_by(CarMake.brand).filter( CarMake.brand != "Unknown").all() ,
               body_styles = ["Any"] + [b for b in body_styles if b != "Unknown"],
               engine_configurations = ["Any"] + [e for e in engine_configurations if e != "Unknown" ],
               fuel_types = ["Any"] + [f for f in fuel_types if f != "Unknown"],
               drivetrains = ["Any"] + [d for d in drivetrains if d != "Unknown"],
               transmissions = ["Any"] + [t for t in transmissions if t != "Unknown"],
               year_list = ["1950","1960","1970","1980"] + [f"{i}" for i in range(1985,datetime.today().year+1)],
               hp_list = [f"{i}" for i in range(0,450,50)] + [f"{i}" for i in range(400,1100,100)],
               price_list = [f"{i}" for i in range(0,10000,200)] + [f"{i}" for i in range(10000,20000,1000)] 
                    + [f"{i}" for i in range(20000,105000,5000)] + [f"{i}" for i in range(150000,1050000,50000)],
               displacement_list = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 15.0, 20.0],
               fuel_efficiency_list = [1.0,2.0,3.0,4.0,5.5,6.0,6.5,7,7.5,8,8.5,9,9.5,10.0,11.0,12.0,13.0,14.0,15.0,16.0,17.0,18.0,19.0,20.0],
               mileage_list = [0,1000,2000,3000,4000,5000,10000,15000,20000,30000,40000,50000,60000,70000,80000,90000,100000] + [ f"{i}" for i in range(150000,550000,50000)] + [ f"{i}" for i in range(600000,1100000,100000)]
               )
                            

@app.route("/viewlisting")
def load_view_listing_page():

     listing_id = request.args.get("listing_id" , -1 , type=int)
     listing = Listing.query.filter_by(id = listing_id).first()

     if not listing :
          return redirect(url_for("load_general_page"))

     if session.get("user_id") != listing.seller_id and listing.status == "private":
          return redirect(url_for("load_general_page"))
     
     if session.get("user_id") != listing.seller_id:
          listing.views = (listing.views or 0) + 1
          db.session.commit()
     
     return render_template("view_listing_page.html",
          listing = listing,
          brand = CarMake.query.filter_by(id=listing.make_id).first().brand if not listing.other_make else listing.other_make,
          model = CarModel.query.filter_by(id=listing.model_id).first().model if not listing.other_model else listing.other_model,
          cover_img_path = listing.images.filter_by(cover_image = True).first().image_path,
          images = listing.images.filter_by(cover_image = False).all(),
          is_favourited = "True" if  Favorites.query.filter_by(listing_id=listing_id, user_id=session.get("user_id")).first() else "False"
          )

@app.route("/mklistp")
def load_make_listing_page():
    if not session.get("user_id"):
          return redirect(url_for("load_home"))

    return render_template("make_listing_page.html" ,
          brands = CarMake.query.order_by(CarMake.brand).all() , 
          body_styles = body_styles, 
          engine_configurations = engine_configurations,
          fuel_types = fuel_types,
          drivetrains = drivetrains,
          transmissions = transmissions
          )

@app.route("/mylistingsp")
def load_my_listings_page():
     if not session.get("user_id"):
            return redirect(url_for("load_home"))
     
     return render_template("my_listings_page.html",
                            user_id = session.get("user_id") )

@app.route("/predictp")
def load_predict_page():
    return render_template("predict_page.html",
               brands = CarMake.query.order_by(CarMake.brand).all(),
               offers = ['Demonstration', "Employee's car", 'New', 'Pre-registered', 'Used'],
               fuel_types = fuel_types,
               drivetrains = drivetrains,
               transmissions = transmissions,
               engine_configurations = engine_configurations , 
               body_styles = body_styles )

@app.route("/regp")
def load_register_page():
    return render_template("register_page.html")

@app.route("/favouritesp")
def load_favourites_page():
      if not session.get("user_id"):
          return redirect(url_for("load_home"))
      
      return render_template("favourites_page.html")

@app.route("/loginp")
def load_login_page():
    return render_template("login_page.html")

@app.route("/editlistingp")
def load_edit_listing_page():
     if not session.get("user_id"):
           return redirect(url_for("load_home"))
     
     listing_id = request.args.get("listing_id", type=int)
     if not listing_id :
          return redirect(url_for("load_my_listings_page"))

     l = Listing.query.filter_by( id = listing_id ).first()

     if not l:
          flash("Listing not found")
          return redirect(url_for("load_my_listings_page"))

     if l.seller_id != session.get("user_id"):
          flash("Not authorised to edit this listing")
          return redirect(url_for("load_my_listings_page"))
     
     return render_template("edit_listing_page.html",
               listing = l,
               brands = CarMake.query.order_by(CarMake.brand).all() ,
               fuel_types = fuel_types,
               drivetrains = drivetrains,
               transmissions = transmissions,
               engine_configurations = engine_configurations , 
               body_styles = body_styles,
               )

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

    
def get_ext(f):
    return os.path.splitext(f.filename)[1].strip().lower()

def save_listing_image(file,is_cover,listing_id):
      
      img_path = f"static/listings_images/{uuid.uuid4()}{get_ext(file)}"
      file.save(img_path)
      db.session.add(ListingImages(listing_id=listing_id, image_path=img_path, cover_image=is_cover))

      return img_path


def image_is_valid(image):

     if get_ext(image) not in ALLOWED_EXT:
          return {
               "status" : "fail",
               "message" : "Invalid image format"}
          
     image.seek(0, os.SEEK_END)
     size = image.tell()
     image.seek(0)

     if size > 5 * 1024 * 1024:
          return {
               "status" : "fail",
               "message" : "Image size too large"}

     return {"status": "ok"}

def is_float(string):
    try:
        return math.isfinite(float(string)) and float(string) >= 0
    except (TypeError, ValueError):
        return False


FIELDS = ["make_id", "model_id", "title", "price", "configuration", "drivetrain", "fuel_type",
                "transmission", "description", "year", "mileage", "power", "displacement", "fuel_efficiency",
                "colour", "body_style", "status"  ]

NUMERICAL_FIELDS = ["price","year","mileage","power","displacement","fuel_efficiency"]

UNITS = ["priceUnit", "mileageUnit", "enginePowerUnit", "engineDisplacementUnit", "fuelEfficiencyUnit"]

ALLOWED_UNITS = {
     "priceUnit" : ("euro", "dollar"),
     "mileageUnit" : ("km", "mile"),
     "enginePowerUnit" : ("hp","kW"),
     "engineDisplacementUnit" : ("L","cc"),
     "fuelEfficiencyUnit" : ("mpg","l/100km")
}

ALLOWED_RANGES = {
      "price": (1,500000),
      "year" : (1880,datetime.today().year+1),
      "mileage": (0,3000000),
      "power" : (1,2000),
      "displacement" : (0.0,20000.0),
      "fuel_efficiency": (0,120)
}

def parse_listing_form():
     is_other ={"make_id": False, "model_id" : False, "fuel_type" : False, "configuration" : False, "drivetrain" : False, "transmission" : False}
     form_data = {}
     form_units = {}
           
     for i in FIELDS:
                          
          data = (request.form.get(i) or "").strip()
                
          if not data and not Listing.__table__.columns[i].nullable :
                              return None, None, None, f"must input required fields{Listing.__table__.columns[i]}"
                          
          elif not data and Listing.__table__.columns[i].nullable :
                                  form_data[i] = None
                
          else:
                    if data == "Other":   # if the user chose the other option
           
                         if i in NUMERICAL_FIELDS:
                              return None, None, None, 'This field does not support the choice "other" '
                                       
                         other = request.form.get(f"other_{i}")  
           
                         if not other:    # if the user inputed no other custom option, error
                              return None, None, None, f"must input other {i}"
                         else:  # if the uesr inputed his other option
                              is_other[i] = True
           
                              form_data[i] = other
                                       
                    elif data == "Unknown" and i in ("make_id", "model_id"): # if the user chose the unknown option
                         is_other[i] = True
           
                         form_data[i] = "Unknown"
           
                    else:  # if the user chose / inputed a normal option
                         if i in NUMERICAL_FIELDS:
                              if not is_float(data):
                                   return None, None, None, f"invalid {i} input"
      
                              data = float(data)
      
                              if not ALLOWED_RANGES[i][0] <= data <= ALLOWED_RANGES[i][1]:
                                   return None, None, None, f"value limit exceeded for {i} "
                                        
                         form_data[i] = data
      
     for u in UNITS:
      
          unit_input = request.form.get(u)
      
          if not unit_input:
               return None, None, None, "must select a unit for measurable inputs"
                
          if unit_input not in ALLOWED_UNITS[u]:
               return None, None, None, "Invalid unit choice"
                
          form_units[u] = unit_input

          
           # INPUT VALIDATION CHECKS
      
     if form_data["fuel_efficiency"] == 0 and form_units["fuelEfficiencyUnit"] == "mpg":
          return None, None, None, "Invalid fuel efficiency input"
     
     if not form_data["make_id"]:
          return None, None, None, "Make required"
     
     if not is_other["make_id"]:
          if not form_data["make_id"].isdigit():
               return None, None, None, "Invalid make id input"
                 
          m = CarMake.query.filter_by(id = form_data["make_id"]).first()
      
          if not m:
               return None, None, None, "Car make not found"
                 
     if not form_data["model_id"]:
          return None, None, None, "Model required"
      
     if not is_other["model_id"]:
          if not form_data["model_id"].isdigit():
               return None, None, None, "Invalid model id input"
                      
          m = CarModel.query.filter_by(id = form_data["model_id"]).first()
      
          if not m:
               return None, None, None, "Car model not found"

          if is_other["make_id"]:
               return None, None, None, "Select a make from the list to choose a model"
          
          if m.make_id != int(form_data["make_id"]):
               return None, None, None, "Model doesn't belong to the selected make"
                      
     if len(form_data["title"]) > 80:
                    return None, None, None, "Title too long , please shorten the input"
     
           
     currency_convert = normalise_currency(form_data["price"], form_units["priceUnit"])
      
     if currency_convert is None:
          return None, None, None, "Conversion from USD to EUR failed , try manual conversion or use EUR until problem is fixed"
      
     form_data["price"] = currency_convert
      
     if form_data["description"] and len(form_data["description"]) > 1000:
          return None, None, None, "Description too long, please shorten the input"
          
     year = form_data["year"]

     if year is not None and not year.is_integer():
          return None, None, None, "Invalid year input"
      
     if form_data["status"] not in ("public","private"):
          return None, None, None, "Status must be either public or private"

     return form_data, form_units, is_other, None

      
@app.route("/upload_listing", methods = ["POST"])
def make_listing():

     # SECURITY CHECK

     if not session.get("user_id"):
          return redirect(url_for("load_home"))

     #  REQUESTING INPUTS
     
     form_data , form_units , is_other, error_message = parse_listing_form()

     if error_message:
          flash(error_message)
          return redirect(url_for("load_make_listing_page"))
     
     # IMAGES

     cover_image = request.files.get("coverCarImage")
     if not cover_image or not cover_image.filename :
          flash("Must submit a cover image")
          return redirect(url_for("load_make_listing_page"))
       
     if image_is_valid(cover_image)["status"] == "fail":
          flash(image_is_valid(cover_image)["message"])
          return redirect(url_for("load_make_listing_page"))
     
     car_list = [f for f in request.files.getlist("carImages") if f.filename]
     
     if len(car_list) > 10 :
          flash("Maximum number of photos exceeded")
          return redirect(url_for("load_make_listing_page"))
     
     for image in car_list:
          if image.filename:
               if image_is_valid(image)["status"] == "fail":
                    flash(image_is_valid(image)["message"])
                    return redirect(url_for("load_make_listing_page"))
                 
     new_listing = Listing(
           seller_id = session.get("user_id") ,
           make_id = int(form_data["make_id"]) if form_data["make_id"] and not is_other["make_id"] else None,
           model_id = int(form_data["model_id"]) if form_data["model_id"] and not is_other["model_id"] else None,
           other_make = form_data["make_id"] if is_other["make_id"] else None ,
           other_model = form_data["model_id"] if is_other["model_id"] else None ,
           title = form_data["title"] ,
           price = form_data["price"],
           configuration = form_data["configuration"] ,
           drivetrain = form_data["drivetrain"] ,
           fuel_type = form_data["fuel_type"] ,
           transmission = form_data["transmission"] ,
           description = form_data["description"] ,
           year = int(form_data["year"]) if form_data["year"] else None,
           mileage = normalise_mileage(form_data["mileage"],form_units["mileageUnit"]) if form_data["mileage"] is not None else None,
           power = normalise_engine_power(form_data["power"],form_units["enginePowerUnit"]) if form_data["power"] is not None else None,
           displacement = normalise_displacement(form_data["displacement"],form_units["engineDisplacementUnit"]) if form_data["displacement"] is not None else None,
           fuel_efficiency = normalise_fuel_efficiency(form_data["fuel_efficiency"] , form_units["fuelEfficiencyUnit"]) if form_data["fuel_efficiency"] is not None else None,
           colour = form_data["colour"] ,
           body_style = form_data["body_style"] ,
           status = form_data["status"]
      )

     saved_images_paths = []

     try:
          db.session.add(new_listing)
          db.session.flush()

          saved_images_paths.append(save_listing_image(cover_image, True, new_listing.id))

          for image in car_list:
               if image.filename:
                    saved_images_paths.append(save_listing_image(image, False, new_listing.id))

          db.session.commit()

     except Exception:
          db.session.rollback()
          for path in saved_images_paths:
               try:
                    os.remove(path)
               except OSError:
                    pass

          saved_images_paths = []
          raise

     flash("Listing uploaded successfuly")
     return redirect(url_for("load_make_listing_page"))


@app.route("/edit_listing/<int:listing_id>", methods=["POST"])
def confirm_edit(listing_id):

     # SECURITY CHECK
     listing = Listing.query.filter_by(id=listing_id).first()

     if not session.get("user_id") or not listing:
           return redirect(url_for("load_home"))

     if listing.seller_id != session.get("user_id"):
          return redirect(url_for("load_home"))

     #  REQUESTING INPUTS
          
     form_data , form_units , is_other, error_message = parse_listing_form()
     
     if error_message:
          flash(error_message)
          return redirect(url_for("load_edit_listing_page", listing_id=listing_id))
     
     # IMAGES

     deleted_cvr_image_id = request.form.get("delete_cov_img")
     deleted_sec_images_ids = set(request.form.getlist("delete_imgs"))
     new_sec_imgs = [f for f in request.files.getlist("carImages") if f.filename]
     new_cvr_img = request.files.get("coverCarImage")

     deleted_sec_images = []
     deleted_cvr_image = None

     if deleted_cvr_image_id:

          if not deleted_cvr_image_id.isdigit():
               flash("Invalid image id")
               return redirect(url_for("load_edit_listing_page", listing_id=listing_id))
          
          img = ListingImages.query.filter_by(id=deleted_cvr_image_id).first()

          if not img or img.listing_id != listing_id or not img.cover_image:
               flash("Tried to delete inexistent cover image")
               return redirect(url_for("load_edit_listing_page", listing_id=listing_id))
     
          if img and not new_cvr_img:
               flash("Must input a cover image")
               return redirect(url_for("load_edit_listing_page", listing_id=listing_id))
          deleted_cvr_image = img     
     
     
     for img_id in deleted_sec_images_ids:

          if not img_id.isdigit():
               flash("Invalid image id")
               return redirect(url_for("load_edit_listing_page", listing_id=listing_id))
          
          img = ListingImages.query.filter_by(id=img_id).first()

          if not img or img.listing_id != listing_id or img.cover_image:
               flash("Invalid image id")
               return redirect(url_for("load_edit_listing_page", listing_id=listing_id))
          
          if not img or img.listing_id != listing_id:
               flash("Tried to delete inexistent secondary image")
               return redirect(url_for("load_edit_listing_page", listing_id=listing_id))
          deleted_sec_images.append(img)

     current_img_count = ListingImages.query.filter_by(listing_id=listing_id,cover_image=False).count()

     if 1 + current_img_count + len(new_sec_imgs) - len(deleted_sec_images_ids) > 11:
          flash("Too many images loaded, max 11 ( 1 cover + 10 secondary )")
          return redirect(url_for("load_edit_listing_page", listing_id=listing_id))

     # SIZE CHECKING FOR INPUT IMAGE FILES

     for image in new_sec_imgs:
          if image.filename:
               if image_is_valid(image)["status"] == "fail":
                    flash(image_is_valid(image)["message"])
                    return redirect(url_for("load_edit_listing_page", listing_id=listing_id))

     if deleted_cvr_image:
          if image_is_valid(new_cvr_img)["status"] == "fail":
               flash(image_is_valid(new_cvr_img)["message"])
               return redirect(url_for("load_edit_listing_page", listing_id=listing_id))

     listing.make_id = int(form_data["make_id"]) if form_data["make_id"] and not is_other["make_id"] else None
     listing.model_id = int(form_data["model_id"]) if form_data["model_id"] and not is_other["model_id"] else None
     listing.other_make = form_data["make_id"] if is_other["make_id"] else None
     listing.other_model = form_data["model_id"] if is_other["model_id"] else None
     listing.title = form_data["title"]
     listing.price = form_data["price"]
     listing.configuration = form_data["configuration"]
     listing.drivetrain = form_data["drivetrain"]
     listing.fuel_type = form_data["fuel_type"]
     listing.transmission = form_data["transmission"]
     listing.description = form_data["description"]
     listing.year = int(form_data["year"]) if form_data["year"] else None
     listing.mileage = normalise_mileage(form_data["mileage"], form_units["mileageUnit"]) if form_data["mileage"] is not None else  None
     listing.power = normalise_engine_power(form_data["power"], form_units["enginePowerUnit"]) if form_data["power"] is not None else None
     listing.displacement = normalise_displacement(form_data["displacement"], form_units["engineDisplacementUnit"]) if form_data["displacement"] is not None else None
     listing.fuel_efficiency = normalise_fuel_efficiency(form_data["fuel_efficiency"], form_units["fuelEfficiencyUnit"]) if form_data["fuel_efficiency"] is not None else None
     listing.colour = form_data["colour"]
     listing.body_style = form_data["body_style"]
     listing.status = form_data["status"]

     new_images_paths = []
     new_cvr_img_path = ''
     old_cvr_img_path = ''

     if deleted_cvr_image_id:
          new_cvr_img_path = f"static/listings_images/{uuid.uuid4()}{get_ext(new_cvr_img)}"
          new_cvr_img.save(new_cvr_img_path)
          old_cvr_img_path = deleted_cvr_image.image_path
          deleted_cvr_image.image_path = new_cvr_img_path

     try:

          for image in new_sec_imgs:
               if image.filename:
                    new_images_paths.append(save_listing_image(image,False,listing.id))

          for img in deleted_sec_images:
               db.session.delete(img)

          db.session.commit()

     except Exception:

          db.session.rollback()
          # erase new saved images for a reset if an error occurs

          for path in new_images_paths:
               try:
                    os.remove(path)
               except OSError:
                    pass

          if deleted_cvr_image_id:
               try:
                    os.remove(new_cvr_img_path)
               except OSError:
                    pass

          raise

     # if saving and comitting to db worked fine we permanently erase from storage the deleted images 
     if deleted_cvr_image_id :
          if os.path.exists(old_cvr_img_path):
                os.remove(old_cvr_img_path)

     for img in deleted_sec_images:
          if os.path.exists(img.image_path):
               os.remove(img.image_path)

     flash("Listing edited successfully")
     return redirect(url_for("load_edit_listing_page",listing_id=listing.id))

     
if __name__ == "__main__":
        app.run()