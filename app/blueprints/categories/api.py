from flask import Blueprint, jsonify

from .services import get_all_categories

api_bp = Blueprint("categories_api", __name__, url_prefix="/api/categories")


@api_bp.get("/")
def get_categories():
    ok, msg, categories = get_all_categories()

    if not ok:
        return jsonify({"success": False, "message": msg, "data": []}), 500

    categories_dict = [c.to_dict() for c in categories]

    return jsonify({"success": True, "message": msg, "data": categories_dict})
