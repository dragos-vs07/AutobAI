# AutobAI

**A used-car marketplace with an AI price estimator and real-time buyer–seller chat.**

Publish listings, browse and filter the market, message sellers instantly, and get a machine-learning estimate of what a car is worth.

Built with Python, Flask, PostgreSQL, Socket.IO and LightGBM.

## Features

- **Marketplace:** create, edit, publish/unpublish and delete listings with multiple photos; browse with filters, sorting and pagination; favourites, a "My listings" page and view counters; mark listings as sold with sale price and date
- **AI price estimator:** a LightGBM regression model estimates a car's price from make, model, fuel type, gearbox, mileage, age, horsepower and offer type, served through a JSON API
- **Real-time chat:** buyer–seller messaging over WebSockets (Flask-SocketIO), saved to the database so conversations persist
- **Accounts and security:** hashed passwords, session authentication, password reset by email with signed time-limited tokens, rate limiting on sensitive endpoints, and server-side validation of forms and image uploads

## Price model

| Model | LightGBM regression |
| Training data | AutoScout24 Germany listings (2011–2021 asking prices), makes with at least 20 listings |
| Inputs | make, model, fuel, gearbox, mileage, age, horsepower, offer type |
| MAE | **€1,631** |
| RMSE | **€4,361** |
| R² | **0.927** |

Metrics were measured on a held-out 20% test set (`random_state=42`). The typical error is about €1,700, while the larger RMSE shows that errors on expensive, rarer cars are bigger. Estimates are available for the makes and models seen in training; other cars are declined instead of guessed.

The year is converted to age, and categorical inputs use the exact category levels saved in `ml/categories.json`, so predictions are encoded the same way as in training. The model is loaded once at startup from `ml/autobay_price_model.txt`.

## Tech stack

Python · Flask · Flask-SQLAlchemy / Alembic · Flask-SocketIO · PostgreSQL · LightGBM · pandas · Flask-Mail · HTML / CSS / JavaScript

## Getting started

Requires Python 3.11+ and a running PostgreSQL database.

```bash
git clone https://github.com/dragos-vs07/AutobAI.git
cd AutobAI

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/autobai
SECRET_KEY=replace-with-a-long-random-string
MAIL_USERNAME=your-gmail-address@gmail.com   # only for password reset emails
MAIL_PASSWORD=your-gmail-app-password
```

Create the tables, load the car makes and models, and run:

```bash
flask --app app db upgrade
python seed.py
python app.py
```

Open http://127.0.0.1:5000.

## Project structure

```
app.py          routes, listing logic, SocketIO chat events
api.py          JSON API: price prediction, listings, favourites, messages
auth.py         registration, login, logout
models.py       SQLAlchemy models
listing_form.py listing form parsing and validation
seed.py         loads makes and models from seed/makes_models.json
ml/             trained LightGBM model and category levels
migrations/     Alembic migrations
templates/ static/
```

## Author

**Dragoș Vișănescu**, Computer Science (AI) student at Babeș-Bolyai University, Cluj-Napoca.
[GitHub](https://github.com/dragos-vs07) · [LinkedIn](https://www.linkedin.com/in/drago%C8%99-nicholas-vi%C8%99%C4%83nescu-ba0176360/)
