import random

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.blueprints.categories.services import get_all_categories
from app.blueprints.document_types.services import get_all_document_types
from app.blueprints.enrollments.services import create_enrollment_service
from app.blueprints.questions.services import get_questions

from .services import register_response, register_student

students_bp = Blueprint("students", __name__, url_prefix="/students")


@students_bp.route("/")
def index():
    return redirect(url_for("students.exam"))


@students_bp.route("/exam")
def exam():
    # PREGUNTAS
    success_questions, message_questions, questions = get_questions()

    if not success_questions:
        flash(message_questions, "error_students_exam")

    # SELECCIONAR 3 ALEATORIAS
    questions = random.sample(questions, k=min(len(questions), 4))

    # TIPOS DE DOCUMENTO
    success_documents, message_documents, document_types = get_all_document_types()

    if not success_documents:
        flash(message_documents, "error_students_exam")

    # CATEGORÍAS
    success_categories, message_categories, categories = get_all_categories()

    if not success_categories:
        flash(message_categories, "error_students_exam")

    return render_template(
        "students/exam.html",
        questions=questions,
        document_types=document_types,
        categories=categories,
    )


@students_bp.route("/save/exam", methods=["POST"])
def save_exam():
    # FORMULARIO
    if request.method == "POST":
        student_name = request.form.get("student_name")
        document_type_id = request.form.get("document_type_id")
        document_number = request.form.get("document_number")

        # REGISTRAR ALUMNO
        success, message, student = register_student(
            student_name, document_type_id, document_number
        )

        if not success:
            flash(message, "error_students_exam")
            return redirect(url_for("students.exam"))

        # REGISTRAR MATRICULAS
        category_ids = request.form.getlist("category_id[]")
        # Quitar duplicados
        category_ids = list(dict.fromkeys(category_ids))

        for category_id in category_ids:
            success_enrollment, message_enrollment, _ = create_enrollment_service(
                student.id, category_id
            )

            if not success_enrollment:
                flash(message_enrollment, "error_students_exam")
                return redirect(url_for("students.exam"))

        # REGISTRAR RESPUESTAS
        for key, value in request.form.items():
            if key.startswith("question_"):
                option_id = value
                new_response = register_response(student.id, option_id)

                if new_response is None:
                    flash(
                        "Ocurrió un error al intentar registrar las respuestas",
                        "error_students_exam",
                    )
                    return redirect(url_for("students.exam"))

        flash("Examen guardado", "success_students_exam")

    return redirect(url_for("students.exam"))
