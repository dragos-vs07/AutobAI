from flask import Flask , render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object("config.Config")

db = SQLAlchemy(app)
migrate = Migrate(app,db)

from models import User, CarMake, CarModel, CarTrim, Listing, ListingImage, Sales, Conversation, Message

@app.route("/")
def load_home():
    return render_template("index.html")

@app.route("/genp")
def load_general_page():
      return render_template("general_page.html")

if __name__ == "__main__":
        app.run()