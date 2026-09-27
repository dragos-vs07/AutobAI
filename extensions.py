from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import session 

db = SQLAlchemy()
migrate = Migrate()

def rate_limit_key():
    if "user_id" in session:
        return f"user:{session['user_id']}"
    return get_remote_address()

limiter = Limiter(rate_limit_key, default_limits=[])