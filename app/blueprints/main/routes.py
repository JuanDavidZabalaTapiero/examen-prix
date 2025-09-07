from flask import Blueprint, render_template

from app.blueprints.questions.services import get_questions

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():

    questions = get_questions()

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
