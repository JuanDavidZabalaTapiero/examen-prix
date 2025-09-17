from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db

from .models import Option, Question, QuestionImage

# == QUESTIONS ==


# CREATE
def create_question(question_text):
    try:
        question = Question(text=question_text)
        db.session.add(question)
        db.session.commit()
        return question
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error al intentar registrar la pregunta: {e}")
        return None


# READ
def get_questions():
    """
    Obtiene todas las preguntas de la base de datos.

    Returns:
        list[Question] | None: Lista de objetos `Question` si la consulta fue
        exitosa, o `None` si ocurrió un error.
    """
    try:
        questions = Question.query.all()
        return True, "Preguntas obtenidas correctamente", questions
    except SQLAlchemyError as e:
        print(f"Error al intentar consultar las preguntas: {e}")
        return False, "Error interno al consultar las preguntas", []


def get_question(question_id):
    try:
        question = Question.query.get(question_id)
        return question
    except SQLAlchemyError as e:
        print(f"Error al intentar consultar la pregunta: {e}")
        return None


# UPDATE


# DELETE
def delete_question(question_id):
    try:
        question = Question.query.get(question_id)
        if not question:
            return False, "Pregunta no encontrada"

        for option in question.options:
            if option.responses:
                return (
                    False,
                    "No se puede eliminar la pregunta porque tiene respuestas asociadas",
                )

        db.session.delete(question)
        db.session.commit()
        return True, "Pregunta eliminada correctamente"

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error al intentar eliminar la pregunta: {e}")
        return False, "Error interno al intentar eliminar la pregunta"


# == OPTIONS ==


# CREATE
def create_option(question_id, text, is_correct):
    try:
        option = Option(question_id=question_id, text=text, is_correct=is_correct)
        db.session.add(option)
        db.session.commit()
        return option
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error al intentar registrar la opción: {e}")
        return None


# READ


def get_option(option_id):
    try:
        option_id = int(option_id)
    except ValueError:
        return False
    try:
        option = Option.query.get(option_id)
        return option
    except SQLAlchemyError as e:
        print(f"Ocurrió un error al intentar consultar la opción: {e}")
        return None


# UPDATE


# DELETE
def delete_option_service(option_id):
    if option_id is None:
        return False, "El ID de la opción es obligatorio"
    try:
        option = get_option(option_id)

        if option is False:
            return False, "El ID de la opción no es válido"

        if option is None:
            return False, "Error al intentar consultar la opción"

        if option.responses:
            return False, "La opción tiene respuestas asociadas"

        db.session.delete(option)
        db.session.commit()

        return True, "Opción eliminada"

    except Exception as e:
        db.session.rollback()
        print(f"Error en delete_option_service: {e}")
        return False, "Error al intentar eliminar la opción"


# == QUESTION IMAGE ==


# CREATE
def create_question_image_service(question_id, image_name):
    if not question_id or not image_name:
        return False, "Campos obligatorios", None

    try:
        question_image = QuestionImage(question_id=question_id, image_name=image_name)
        db.session.add(question_image)
        db.session.commit()
        return True, "Imagen guardadas correctamente", question_image

    except Exception as e:
        db.session.rollback()
        print(f"Error en create_question_image_service: {e}")
        return False, "Error al intentar registrar la imagen", None


# READ

# UPDATE

# DELETE
