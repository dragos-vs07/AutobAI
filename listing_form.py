import math
import requests
from datetime import datetime
from flask import request
from models import Listing, CarMake, CarModel

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