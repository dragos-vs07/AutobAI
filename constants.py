from pycountry import countries

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

fuel_types = [
    "CNG",
    "Diesel",
    "Electric",
    "Electric/Gasoline",
    "Electric/Diesel",
    "Ethanol",
    "Gasoline",
    "Hydrogen",
    "LPG",
    "Other",
    "Unknown",
]

drivetrains = [
    "FWD",
    "RWD",
    "AWD",
    "4WD",
    "Other",
    "Unknown",
]

transmissions = [
    "Manual",
    "Automatic",
    "Semi-Automatic",
    "Other",
    "Unknown",
]

user_types = ['Individual','Dealership','Company','Manufacturer',"Other"]

countries = ["Other"] + [c.name for c in countries]