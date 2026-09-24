from flask import Blueprint, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import User
from constants import user_types, countries
import validators

auth = Blueprint("auth", __name__)

@auth.route("/submit_registration" , methods = ["POST"])
def register_account():
     
      username = request.form.get("username","")
      email = request.form.get("email","")
      password = request.form.get("password","")
      cpassword = request.form.get("cpassword","")
      phone_number = request.form.get("phone","")
      website_url = request.form.get("website_url","")
      user_type = request.form.get("user_type","")
      country = request.form.get("country","")
      city = request.form.get("city","")
      street = request.form.get("street","")

      if not username or not email or not password or not cpassword:
            flash("Please fill in all the required fields")
            return(redirect(url_for("load_register_page")))

      if any(char.isspace() for char in username) or any(char.isspace() for char in email) or any(char.isspace() for char in password) or any(char.isspace() for char in cpassword):
            flash("No whitespaces allowed in required fields input")
            return(redirect(url_for("load_register_page")))

      if len(username) < 5 or len(password) < 5 or len(email) < 5 or len(cpassword) < 5:
            flash("All required fields inputs must have at least 5 characters")
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

      if website_url:
            if not validators.url(website_url):
                  flash("Website url not valid")
                  return(redirect(url_for("load_register_page")))

      if user_type not in user_types:
            flash("Invalid user type")
            return(redirect(url_for("load_register_page")))

      if country not in countries:
            flash("Country not found")
            return(redirect(url_for("load_register_page")))

      if len(city) > 30:
            flash("City name too long")
            return(redirect(url_for("load_register_page")))

      if len(street) > 80:
            flash("Street adress too long")
            return(redirect(url_for("load_register_page")))
      
      db.session.add(User(
           username = username, 
           email = email,
           password_hash = generate_password_hash(password),
           phone_number = phone_number,
           website_url = website_url,
           type = user_type,
           country = country,
           city = city,
           address = street
     ))

      db.session.commit()
     
      session["user_id"] = User.query.filter_by(username = username).first().id
    
      return(redirect(url_for("load_general_page")))

@auth.route("/submit_login" , methods = ["POST"])
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

@auth.route("/logout")
def logout_user():
      if not session.get("user_id"):
            return redirect(url_for("load_home"))
       
      session.clear()
      return redirect(url_for("load_general_page"))