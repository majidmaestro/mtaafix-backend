from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.models import db, Item
from app.schemas import ItemSchema
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)