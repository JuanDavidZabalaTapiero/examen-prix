from sqlalchemy.exc import IntegrityError

from app.extensions import db

from .models import QuestionCompetence


# == CREATE ==
def create_question_competence_service(name, competence_father):
    if not name:
        return False, "Todos los campos son obligatorios", None

    try:
        question_competence = QuestionCompetence(name=name, parent_id=competence_father)
        db.session.add(question_competence)
        db.session.commit()
        return True, "Competencia registrada correctamente", question_competence

    except IntegrityError:
        db.session.rollback()
        return False, "La competencia ya está registrada", None

    except Exception as e:
        db.session.rollback()
        print(f"Error en create_question_competence_service: {e}")
        return False, "Error al intentar registrar la competencia", None


# == READ ==
def get_all_question_competences():
    try:
        competences = QuestionCompetence.query.all()
        return True, "Competencias consultadas correctamente", competences

    except Exception as e:
        print(f"Error en get_all_question_competences: {e}")
        return False, "Error al intentar consultar las competencias", None


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


def get_competencies_without_parent():
    try:
        competences = QuestionCompetence.query.filter(
            QuestionCompetence.parent_id.is_(None)
        ).all()
        return True, "Competencias consultadas", competences
    except Exception as e:
        print(f"Error en get_competencies_without_parent: {e}")
        return (
            False,
            "Error al intentar consultas las competencias sin competencia padre",
            [],
        )


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

        return True, "Competencia editada correctamente", question_competence

    except Exception as e:
        db.session.rollback()
        print(f"Error en update_question_competence_service: {e}")
        return False, "Error al intentar editar la competencia", None


# == DELETE ==
def delete_question_competence_service(question_competence_id):
    if not question_competence_id:
        return False, "Todos los campos son obligatorios"

    try:
        success, message, question_competence = get_question_competence(
            question_competence_id
        )

        if not success:
            return False, message

        db.session.delete(question_competence)
        db.session.commit()

        return True, "Competencia eliminada correctamente"

    except Exception as e:
        db.session.rollback()
        print(f"Error en delete_question_competence_service: {e}")
        return False, "Error al intentar eliminar la competencia"
