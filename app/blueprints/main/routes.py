from flask import Blueprint, flash, render_template

from app.blueprints.questions.services import get_questions

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    # PREGUNTAS
    success, message, questions = get_questions()

    if not success:
        flash(message, "error_main_home")

    data = []

    for q in questions:
        labels = [opt.text for opt in q.options]
        counts = [len(opt.responses) for opt in q.options]
        data.append(
            {
                "question_id": q.id,
                "question": q.text,
                "labels": labels,
                "counts": counts,
            }
        )

    return render_template("main/home.html", data=data)
