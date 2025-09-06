from flask import Flask, render_template

from .blueprints import register_blueprints
from .config import Config
from .extensions import db, migrate


def create_app(config_class=Config):
    app = Flask(__name__)

    # == CONFIGURACIÓN ==
    app.config.from_object(config_class)

    # == INICIALIZAR EXTENSIONES ==
    db.init_app(app)
    migrate.init_app(app, db)

    # == IMPORTAR MODELOS ==
    from . import models  # noqa: F401

    # == REGISTRAR BLUEPRINTS ==
    register_blueprints(app)

    # == 404 ==
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html"), 404

    return app
