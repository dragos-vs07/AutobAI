from pycountry import countries

body_styles = [
    "Unknown",
    "Other",
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
    "Limousine"
]

engine_configurations = [
    "Unknown",
    "Other",
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
    "Rotary"
]

fuel_types = [
    "Unknown",
    "Other",
    "CNG",
    "Diesel",
    "Electric",
    "Electric/Gasoline",
    "Electric/Diesel",
    "Ethanol",
    "Gasoline",
    "Hydrogen",
    "LPG"
]

drivetrains = [
    "Unknown",
    "Other",
    "FWD",
    "RWD",
    "AWD",
    "4WD"
]

transmissions = [
    "Unknown",
    "Other",
    "Manual",
    "Automatic",
    "Semi-Automatic"
]

user_types = [
    "Other",
    'Individual',
    'Dealership',
    'Company',
    'Manufacturer'
]

countries = ["Other"] + [c.name for c in countries]