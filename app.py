from flask import Flask , render_template
from extensions import db , migrate

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

if __name__ == "__main__":
        app.run()