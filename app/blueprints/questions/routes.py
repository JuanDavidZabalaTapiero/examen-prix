import os

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from werkzeug.utils import secure_filename

from app.blueprints.question_competences.services import get_all_question_competences
from app.extensions import db

from .services import (
    create_option,
    create_question,
    create_question_competence_association,
    create_question_image_service,
    delete_option_service,
    delete_question,
    get_option,
    get_question,
    get_questions,
)

questions_bp = Blueprint("questions", __name__, url_prefix="/questions")


# == HOME ==
@questions_bp.route("/")
def home():

    success_questions, message_questions, questions = get_questions()

    if not success_questions:
        flash(
            message_questions,
            "error_questions_home",
        )

    return render_template("questions/home.html", questions=questions)


# == REGISTRAR PREGUNTA ==
@questions_bp.route("/new/question")
def new_question():
    success_c, message_c, competences = get_all_question_competences()

    if not success_c:
        flash(message_c, "error_questions_new_question")

    return render_template("questions/new_question.html", competences=competences)


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

        # REGISTRAR IMAGENES
        images = request.files.getlist("images")

        for file in images:
            if file and file.filename:
                image_name = secure_filename(file.filename)
                filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], image_name)
                file.save(filepath)

                success_image, message_image, _ = create_question_image_service(
                    question.id, image_name
                )

                if not success_image:
                    flash(message_image, "error_questions_home")
                    return redirect(url_for("questions.home"))

        # REGISTRAR COMPETENCIAS
        competences_id = list(set(request.form.getlist("competence_id")))

        print(competences_id)

        for competence_id in competences_id:
            success_c, message_c, _ = create_question_competence_association(
                question.id, competence_id
            )

            if not success_c:
                flash(message_c, "error_questions_home")
                return redirect(url_for("questions.home"))

        flash("Pregunta registrada exitosamente", "success_questions_home")

    return redirect(url_for("questions.home"))


# == EDITAR PREGUNTA ==
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


# == ELIMINAR PREGUNTA ==
@questions_bp.route("/delete/question/<int:question_id>")
def delete_question_route(question_id):
    success, message = delete_question(question_id)

    if success:
        flash(message, "success_questions_home")
    else:
        flash(message, "error_questions_home")

    return redirect(url_for("questions.home"))


# == ELIMINAR OPCIÓN ==
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


# == SERVIR IMAGEN ==
@questions_bp.route("/images/<filename>")
def get_question_image(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)
