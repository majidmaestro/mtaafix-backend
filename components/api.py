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

@api_bp.route('/items', methods=['GET'])
def get_all_items():
    """
    Retrieve all item records from the database.
    Support optional search filtering via query parameters.
    """
    logger.info("handling GET request for /api/v1/items")
    try:
        search_query = request.args.get('search', type=str)
        query = Item.query

        if search_query:
            logger.info(f"Filtering items matching query: {search_query}")
            items = query.filter(Item.name.ilike(f"%{search_query}%")).all()
        else:
            items = query.all()

        serialized_items = items_schema.dump(items)
        return build_response(
            success=True,
            message=f"Successfully retrieved {len(serialized_items)} items(s).",
            data=serialized_items,
            status_code=200
        )
    
    except Exception as e:
        logger.exception(f"Database query failed: {str(e)}")
        return build_response(
             success=False,
             message="An unexpected error occurred while fetching items.",
             status_code=500

        )

       
		   

        