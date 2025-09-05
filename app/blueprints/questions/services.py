from sqlalchemy.exc import SQLAlchemyError

from .models import Question


def get_questions():
    """
    Obtiene todas las preguntas de la base de datos.

    Returns:
        list[Question] | None: Lista de objetos `Question` si la consulta fue
        exitosa, o `None` si ocurrió un error.
    """
    try:
        questions = Question.query.all()
        return questions
    except SQLAlchemyError as e:
        print(f"Error al intentar consultar las preguntas: {e}")
        return None
