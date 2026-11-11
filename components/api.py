from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.models import db, Item
from app.schemas import ItemSchema
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_bp = Blueprint('api-bp', __name__, url_prefix='/api/v1')

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

def build_response(success: bool, message: str, data=None, status_code: int = 200):
	"""Helper function to maintain a consistent JSON response structure."""
	response_payload = {
		"status": "success" if success else "error",
		"message": message
    }
	if data is not None:
		response_payload["data"] = data
	return jsonify(response_payload), status_code