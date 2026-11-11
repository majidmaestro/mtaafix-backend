from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from .extensions import db, jwt


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    jwt.init_app(app)

    @app.get("/api/health")
    def health():
        return jsonify(
            status="ok",
            message="MtaaFix API is running."
        )

    return app