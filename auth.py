from flask import Blueprint, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import User
auth = Blueprint("auth", __name__)

@auth.route("/submit_registration" , methods = ["POST"])
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