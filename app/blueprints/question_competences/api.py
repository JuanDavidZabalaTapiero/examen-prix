from flask import Blueprint, jsonify

from .services import get_all_question_competences

api_bp = Blueprint("competences_api", __name__, url_prefix="/api/competences")


@api_bp.get("/")
def get_competences():

    ok, msg, competences = get_all_question_competences()

    if not ok:
        return jsonify({"success": False, "message": msg, "data": []})

    competences_dict = [c.to_dict() for c in competences]

    return jsonify({"success": True, "message": msg, "data": competences_dict})
