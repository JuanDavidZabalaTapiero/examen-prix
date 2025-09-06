from .main.routes import main_bp
from .students.routes import students_bp


def register_blueprints(app):
    app.register_blueprint(students_bp)
    app.register_blueprint(main_bp)
