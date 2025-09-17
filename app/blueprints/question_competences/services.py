from sqlalchemy.exc import IntegrityError

from app.extensions import db

from .models import QuestionCompetence


# == CREATE ==
def create_question_competence_service(name):
    if not name:
        return False, "Todos los campos son obligatorios", None

    try:
        question_competence = QuestionCompetence(name=name)
        db.session.add(question_competence)
        db.session.commit()
        return True, "Competencia creada correctamente", question_competence

    except IntegrityError:
        db.session.rollback()
        return False, "La competencia ya está registrada", None

    except Exception as e:
        db.session.rollback()
        print(f"Error en create_question_competence_service: {e}")
        return False, "Error al intentar registrar la competencia", None


# == READ ==
def get_question_competence(question_competence_id):
    if not question_competence_id:
        return False, "Todos los campos son obligatorios", None

    try:
        question_competence = QuestionCompetence.query.get(question_competence_id)

        if not question_competence:
            return False, "La competencia no existe", None

        return True, "Competencia consultada correctamente", question_competence

    except Exception as e:
        print(f"Error en get_question_competence: {e}")
        return False, "Error al intentar consultar la competencia", None


# == UPDATE ==
def update_question_competence_service(question_competence_id, name):
    if not question_competence_id or not name:
        return False, "Todos los campos son obligatorios", None

    try:
        success, message, question_competence = get_question_competence(
            question_competence_id
        )

        if not success:
            return False, message, None

        question_competence.name = name
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print(f"Error en update_question_competence_service: {e}")
        return False, "Error al intentar editar la competencia", None


# == DELETE ==
def delete_question_competence_service(question_competence_id):
    if not question_competence_id:
        return False, "Todos los campos son obligatorios", None

    try:
        success, message, question_competence = get_question_competence(
            question_competence_id
        )

        if not success:
            return False, message, None

        db.session.delete(question_competence)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print(f"Error en delete_question_competence_service: {e}")
        return False, "Error al intentar eliminar la competencia", None
