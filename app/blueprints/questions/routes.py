from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.extensions import db

from .services import (
    create_option,
    create_question,
    delete_option_service,
    delete_question,
    get_option,
    get_question,
    get_questions,
)

questions_bp = Blueprint("questions", __name__, url_prefix="/questions")


@questions_bp.route("/")
def home():

    success, message, questions = get_questions()

    if not success:
        flash(
            message,
            "error_questions_home",
        )

    return render_template("questions/home.html", questions=questions)


@questions_bp.route("/new/question")
def new_question():
    return render_template("questions/new_question.html")


@questions_bp.route("/register/question", methods=["POST"])
def register_question():

    if request.method == "POST":
        question_text = request.form.get("question_text")

        # REGISTRAR PREGUNTA
        question = create_question(question_text)

        if question is None:
            flash(
                "Ocurrió un error al intentar registrar la pregunta",
                "error_questions_home",
            )
            return redirect(url_for("questions.home"))

        options = request.form.getlist("option_text")
        correct_index = int(request.form.get("correct_option", -1))

        # REGISTRAR OPCIONES
        for idx, text in enumerate(options):
            option = create_option(question.id, text, is_correct=(idx == correct_index))

            if option is None:
                flash(
                    "Ocurrió un error al intentar registrar la pregunta y sus opciones",
                    "error_questions_home",
                )
                return redirect(url_for("questions.home"))

        flash("Pregunta registrada exitosamente", "success_questions_home")

    return redirect(url_for("questions.home"))


@questions_bp.route("/edit/question/<int:question_id>", methods=["GET", "POST"])
def edit_question(question_id):

    question = get_question(question_id)

    if question is None:
        flash("Ocurrió un error al intentar consultar la pregunta")
        return redirect(url_for("questions.home"))

    return render_template("questions/edit_question.html", question=question)


@questions_bp.route("/update/question", methods=["POST"])
def update_question():
    if request.method == "POST":
        # PREGUNTA
        question_id = request.form.get("question_id")
        question = get_question(question_id)

        if question is None:
            flash(
                "Ocurrió un error al intentar editar la pregunta",
                "error_questions_home",
            )
            return redirect(url_for("questions.home"))

        # EDITAR PREGUNTA
        question.text = request.form.get("question_text")

        # OPCIONES
        option_ids = request.form.getlist("option_id")
        option_texts = request.form.getlist("option_text")
        correct_id = request.form.get("correct_option")

        for (
            oid,
            text,
        ) in zip(option_ids, option_texts):
            option = get_option(oid)

            # NO EXISTE (CREAR)
            if option is False:
                is_correct = oid == correct_id
                new_option = create_option(question_id, text, is_correct)

                if new_option is None:
                    flash(
                        "Ocurrió un error al intentar crear una nueva opción",
                        "error_questions_home",
                    )
                    return redirect(url_for("questions.home"))

            # ERROR EN DB AL CONSULTARLA
            if option is None:
                flash(
                    "Ocurrió un error al intentar editar la pregunta y sus opciones",
                    "error_questions_home",
                )
                return redirect(url_for("questions.home"))

            # EXISTE (ACTUALIZAR)
            if option:
                option.text = text
                option.is_correct = str(option.id) == correct_id

        db.session.commit()

        flash("Pregunta actualizada", "success_questions_edit_question")

        return redirect(url_for("questions.edit_question", question_id=question_id))

    return redirect(url_for("questions.home"))


@questions_bp.route("/delete/question/<int:question_id>", methods=["POST"])
def delete_question_route(question_id):
    success, message = delete_question(question_id)

    if success:
        flash(message, "success_questions_home")
    else:
        flash(message, "error_questions_home")

    return redirect(url_for("questions.home"))


# = ELIMINAR OPCIÓN =
@questions_bp.route("/delete/option/<int:option_id>")
def delete_option(option_id):
    option = get_option(option_id)

    if option is None:
        flash("Error al intentar consultar la opción")
        return redirect(url_for("questions.home"))

    question_id = option.question.id

    success, message = delete_option_service(option_id)

    if success:
        flash(message, "success_questions_edit_question")
    else:
        flash(message, "error_questions_edit_question")

    return redirect(url_for("questions.edit_question", question_id=question_id))
