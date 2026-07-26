from flask import Flask , render_template , session , request , flash , redirect , url_for
from extensions import db , migrate
import pandas as pd
from werkzeug.security import generate_password_hash , check_password_hash

app = Flask(__name__)
app.config.from_object("config.Config")

db.init_app(app)
migrate.init_app(app, db)

from models import User, CarMake, CarModel, Listing, ListingImages,  Conversations, Messages

@app.route("/")
def load_home():
    return render_template("index.html")

@app.route("/genp")
def load_general_page():
      return render_template("general_page.html")

@app.route("/mklistp")
def load_make_listing_page():
    return render_template("make_listing_page.html")

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
    return render_template("account_page.html")

@app.route("/infop")
def load_information_page():
          return render_template("information_page.html")

@app.route("/submit_registration" , methods = ["POST"])
def register_account():
     
     username = request.form.get("username","")
     email = request.form.get("email","")
     password = request.form.get("password","")
     cpassword = request.form.get("cpassword","")

     if not username or not email or not password or not cpassword:
          flash("Please fill in all the fields")
          return(redirect(url_for("load_register_page")))

     if any(char.isspace() for char in username) or any(char.isspace() for char in email) or any(char.isspace() for char in password) or any(char.isspace() for char in cpassword):
      flash("No whitespaces allowed in input")
      return(redirect(url_for("load_register_page")))

     if len(username) < 5 or len(password) < 5 or len(email) < 5 or len(cpassword) < 5:
           flash("All inputs must have at least 5 characters")
           return(redirect(url_for("load_register_page")))
     
     if User.query.filter_by(username = username).first() :
           flash("Account with entered username already registered" , "nuquser")
           return(redirect(url_for("load_register_page")))
     
     if User.query.filter_by(email = email).first() :
                flash("Account with entered email already registered" , "nuqemail")
                return(redirect(url_for("load_register_page")))

     if password != cpassword:
           flash("Confirmed password not the same" , "dpass")
           return(redirect(url_for("load_register_page")))
           
     db.session.add(User(
           username = username , 
           email = email ,
           password_hash = generate_password_hash(password)
     ))

     db.session.commit()

     session["user_id"] = User.query.filter_by(username = username).first().id

     return(redirect(url_for("load_register_page")))

@app.route("/submit_login" , methods = ["POST"])
def login_user():
      ue = request.form.get("username_or_email")
      input_password = request.form.get("password")

      if not ue:
            flash("Must input username or email")
            return(redirect(url_for("load_login_page")))

      if not input_password:
            flash("Must input password")
            return(redirect(url_for("load_login_page")))

      user = User.query.filter_by(username = ue).first()

      if not user:
        user = User.query.filter_by(email = ue).first()

      if not user:
           flash("Login data incorrect")
           return(redirect(url_for("load_login_page")))
      
      if check_password_hash( user.password_hash , input_password ):
            session["user_id"] = user.id
            return(redirect(url_for("load_general_page")))
      else:
           flash("Login data incorrect")
           return(redirect(url_for("load_login_page")))

      
            

if __name__ == "__main__":
        app.run()