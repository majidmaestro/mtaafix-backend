import os
from flask import flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors CORS
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///mtaafix.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


