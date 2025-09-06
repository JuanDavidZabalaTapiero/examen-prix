import random

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.blueprints.questions.services import get_questions

from .services import register_response, register_student

students_bp = Blueprint("students", __name__, url_prefix="/students")


@students_bp.route("/")
def home():
    questions = get_questions()

    # SELECCIONAR 3 ALEATORIAS
    if questions:
        questions = random.sample(questions, k=3)

    return render_template("students/home.html", questions=questions)


@students_bp.route("/save/exam", methods=["POST"])
def save_exam():
    # FORMULARIO
    if request.method == "POST":
        student_name = request.form.get("student_name")

        # REGISTRAR ALUMNO
        student = register_student(student_name)

        if student is None:
            flash(
                "Ocurrió un error al intentar registrar el nombre del alumno",
                "error_students_home",
            )
            return redirect(url_for("students.home"))

        # REGISTRAR RESPUESTAS
        for key, value in request.form.items():
            if key.startswith("question_"):
                option_id = value
                new_response = register_response(student.id, option_id)

                if new_response is None:
                    flash(
                        "Ocurrió un error al intentar registrar las respuestas",
                        "error_students_home",
                    )
                    return redirect(url_for("students.home"))

        flash("Examen guardado", "success_students_home")

        return redirect(url_for("students.home"))
