import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from .extensions import db, jwt

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv(
        'SECRET_KEY', 'default-secret-key'
    )

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///mtaafix.db'
    )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    with app.app_context():
        from . import models
        db.create_all()

    @app.route('/')
    def index():
        return {"message": "Mtaafix Backend API is running"}

    return app
