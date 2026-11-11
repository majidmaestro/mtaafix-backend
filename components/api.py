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

@api_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item_by_id(item_id):
     """Fetch a single item record using its unique primary key ID."""
     logger.info(f"Fetching item with ID: {item_id}")

     try:
          item = Item.query.get(item_id)

          if not item:
               logger.warning(f"Item with ID {item_id} not found.")
               return build_response(
                    success=False,
                    message=f"Resources with ID {item_id} does not exist.",
                    status_code=404
               )
          return build_response(
               success=True,
               message="Item retrieved successfully.",
               data=item_schema.dump(item),
               status_code=200
          )
     except Exception as e:
          logger.error(f"Error retrieving item {item_id}: {str(e)}")
          return build_response(
               success=False
               message="Internal server error.",
               status_code=500
          )
       
@api_bp.route('/items', methods=['POST'])
def create_item():
    """Create a new item after validating payload against the schema."""
    logger.info("Processing POST request to create new item...")
    
    json_payload = request.get_json()
    
    if not json_payload:
        return build_response(
            success=False, 
            message="Missing request body or content-type is not application/json.",
            status_code=400
        )

    try:
        # Deserialize and validate incoming data using Marshmallow
        validated_data = item_schema.load(json_payload)
        
        # Instantiate and save to database
        new_item = Item(**validated_data)
        db.session.add(new_item)
        db.session.commit()
        
        logger.info(f"Successfully created item with ID: {new_item.id}")
        
        return build_response(
            success=True, 
            message="Item created successfully.",
            data=item_schema.dump(new_item),
            status_code=201
        )

    except ValidationError as err:
        logger.warning(f"Validation error on create: {err.messages}")
        return build_response(
            success=False, 
            message="Validation failed for submitted fields.",
            data={"errors": err.messages},
            status_code=422
        )
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Database commit failed during item creation: {str(e)}")
        return build_response(
            success=False, 
            message="Database error occurred while saving the item.",
            status_code=500
        )

        