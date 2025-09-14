from flask import Blueprint, flash, redirect, render_template, request, url_for

from .services import (
    create_document_type_service,
    delete_document_type_service,
    get_all_document_types,
    get_document_type,
    update_document_type_service,
)

doc_types_bp = Blueprint("doc_types", __name__, url_prefix="/doc_types")


# == HOME ==
@doc_types_bp.route("/")
def home():
    success, message, document_types = get_all_document_types()

    if not success:
        flash(message, "error_doc_types_home")

    return render_template("doc_types/home.html", document_types=document_types)


# == REGISTRAR DOCUMENTO ==
@doc_types_bp.route("/new")
def new_document_type():
    return render_template("doc_types/new_document_type.html")


@doc_types_bp.route("/create", methods=["POST"])
def create_document_type():
    if request.method == "POST":
        doc_type_name = request.form.get("doc_type_name")
        success, message, _ = create_document_type_service(doc_type_name)

        if success:
            flash(message, "success_doc_types_new_document_type")
        else:
            flash(message, "error_doc_types_new_document_type")

    return redirect(url_for("doc_types.new_document_type"))


# == EDITAR DOCUMENTO ==
@doc_types_bp.route("/edit/<int:doc_type_id>")
def edit_document_type(doc_type_id):
    success, message, document = get_document_type(doc_type_id)

    if not success:
        flash(message, "error_doc_types_edit_document_type")

    return render_template("doc_types/edit_document_type.html", document=document)


@doc_types_bp.route("/update", methods=["POST"])
def update_document_type():
    if request.method == "POST":
        doc_type_id = request.form.get("doc_type_id")
        doc_type_name = request.form.get("doc_type_name")

        success, message, _ = update_document_type_service(doc_type_id, doc_type_name)

        if success:
            flash(message, "success_doc_types_edit_document_type")
        else:
            flash(message, "error_doc_types_edit_document_type")

        return redirect(
            url_for("doc_types.edit_document_type", doc_type_id=doc_type_id)
        )

    return redirect(url_for("doc_type.home"))


# == ELIMINAR DOCUMENTO ==
@doc_types_bp.route("/delete/<int:document_type_id>")
def delete_document_type(document_type_id):
    success, message = delete_document_type_service(document_type_id)

    if success:
        flash(message, "success_doc_types_home")
    else:
        flash(message, "error_doc_types_home")

    return redirect(url_for("doc_types.home"))
