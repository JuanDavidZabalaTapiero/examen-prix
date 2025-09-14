from flask import Blueprint, flash, redirect, render_template, request, url_for

from .services import (
    create_category_service,
    delete_category_service,
    get_all_categories,
    get_category,
    update_category_service,
)

categories_bp = Blueprint("categories", __name__, url_prefix="/categories")


# == HOME ==
@categories_bp.route("/")
def home():
    success, message, categories = get_all_categories()

    if not success:
        flash(message, "error_categories_home")

    return render_template("categories/home.html", categories=categories)


# == REGISTRAR CATEGORÍA ==
@categories_bp.route("/new")
def new_category():
    return render_template("categories/new_category.html")


@categories_bp.route("/create", methods=["POST"])
def create_category():
    if request.method == "POST":
        category_name = request.form.get("category_name")
        success, message, _ = create_category_service(category_name)

        if not success:
            flash(message, "error_categories_new_category")
            return redirect(url_for("categories.new_category"))

        flash(message, "success_categories_new_category")

    return redirect(url_for("categories.new_category"))


# == EDITAR CATEGORÍA ==
@categories_bp.route("/edit/<int:category_id>")
def edit_category(category_id):
    success, message, category = get_category(category_id)

    if not success:
        flash(message, "error_categories_edit_category")

    return render_template("categories/edit_category.html", category=category)


@categories_bp.route("/update", methods=["POST"])
def update_category():
    if request.method == "POST":
        category_id = request.form.get("category_id")
        category_name = request.form.get("category_name")
        success, message, _ = update_category_service(category_id, category_name)

        if not success:
            flash(message, "error_categories_edit_category")
            return redirect(
                url_for("categories.edit_category", category_id=category_id)
            )

        flash(message, "success_categories_edit_category")

        return redirect(url_for("categories.edit_category", category_id=category_id))

    return redirect(url_for("categories.home"))


# == ELIMINAR CATEGORÍA ==
@categories_bp.route("/delete/<int:category_id>")
def delete_category(category_id):
    success, message = delete_category_service(category_id)

    if success:
        flash(message, "success_categories_home")
    else:
        flash(message, "error_categories_home")

    return redirect(url_for("categories.home"))
