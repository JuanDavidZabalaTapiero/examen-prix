from flask import Blueprint, render_template

from app.blueprints.questions.services import get_questions

students_bp = Blueprint("students", __name__)


@students_bp.route("/")
def home():
    questions = get_questions()

    return render_template("students/home.html", questions=questions)
