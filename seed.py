"""Load car makes and models into an empty database.

    flask --app app db upgrade
    python seed.py
"""
import json

from app import app
from extensions import db
from models import CarMake, CarModel

with app.app_context():
    if CarMake.query.first():
        print("Makes already present, nothing to do.")
        raise SystemExit

    with open("seed/makes_models.json", encoding="utf-8") as f:
        data = json.load(f)

    for brand, models in data.items():
        make = CarMake(brand=brand)
        db.session.add(make)
        db.session.flush()
        db.session.add_all(CarModel(make_id=make.id, model=m) for m in models)

    db.session.commit()
    print(f"Seeded {len(data)} makes and {sum(len(v) for v in data.values())} models.")
