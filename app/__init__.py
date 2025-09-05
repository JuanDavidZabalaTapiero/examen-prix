from flask import Flask

from .blueprints.students.routes import students_bp
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
    app.register_blueprint(students_bp)

    return app
