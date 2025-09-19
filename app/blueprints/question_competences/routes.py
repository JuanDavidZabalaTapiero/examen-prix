from flask import Blueprint, flash, redirect, render_template, request, url_for

from .services import (
    create_question_competence_service,
    delete_question_competence_service,
    get_all_question_competences,
    get_question_competence,
    update_question_competence_service,
)

competences_bp = Blueprint("competences", __name__, url_prefix="/competences")


# == HOME ==
@competences_bp.route("/")
def home():
    success, message, competences = get_all_question_competences()

    if not success:
        flash(message, "error_competences_home")

    return render_template("competences/home.html", competences=competences)


# == REGISTRAR ==
@competences_bp.route("/new")
def new_competence():
    return render_template("competences/new_competence.html")


@competences_bp.route("/create", methods=["POST"])
def create_competence():
    if request.method == "POST":
        competence_name = request.form.get("competence_name")

        success, message, _ = create_question_competence_service(competence_name)

        if success:
            flash(message, "success_competences_new_competence")
        else:
            flash(message, "error_competences_new_competence")

        return redirect(url_for("competences.new_competence"))

    return redirect(url_for("competences.home"))


# == EDITAR ==
@competences_bp.route("/edit/<int:competence_id>")
def edit_competence(competence_id):
    success, message, competence = get_question_competence(competence_id)

    if not success:
        flash(message, "error_competences_edit_competence")

    return render_template("competences/edit_competence.html", competence=competence)


@competences_bp.route("/update", methods=["POST"])
def update_competence():
    if request.method == "POST":
        competence_id = request.form.get("competence_id")
        competence_name = request.form.get("competence_name")

        success, message, _ = update_question_competence_service(
            competence_id, competence_name
        )

        if success:
            flash(message, "success_competences_edit_competence")
        else:
            flash(message, "error_competences_edit_competence")

    return redirect(url_for("competences.edit_competence", competence_id=competence_id))


# == ELIMINAR ==
@competences_bp.route("/delete/<int:competence_id>")
def delete_competence(competence_id):
    success, message = delete_question_competence_service(competence_id)

    if success:
        flash(message, "success_competences_home")
    else:
        flash(message, "error_competences_home")

    return redirect(url_for("competences.home"))
