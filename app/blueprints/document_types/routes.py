from flask import Blueprint, render_template

doc_types_bp = Blueprint("doc_types", __name__, url_prefix="/doc_types")


@doc_types_bp.route("/")
def home():
    return render_template("doc_types/home.html")
