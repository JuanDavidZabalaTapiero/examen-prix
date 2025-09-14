from .categories.routes import categories_bp
from .document_types.routes import doc_types_bp
from .main.routes import main_bp
from .questions.routes import questions_bp
from .students.routes import students_bp


def register_blueprints(app):
    app.register_blueprint(students_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(questions_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(doc_types_bp)
