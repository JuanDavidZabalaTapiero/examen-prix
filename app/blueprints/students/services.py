from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db

from .models import Response, Student


def register_student(name):
    try:
        if not name or name.strip() == "":
            return False, "El nombre no puede estar vacío", None

        new_student = Student(name=name)
        db.session.add(new_student)
        db.session.commit()
        return True, "Alumno registrado correctamente", new_student

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error al intentar registrar el alumno: {e}")
        return False, "Error interno al intentar registrar el alumno", None


def register_response(student_id, option_id):
    try:
        new_response = Response(student_id=student_id, option_id=option_id)
        db.session.add(new_response)
        db.session.commit()
        return new_response
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error al intentar registrar la respuesta: {e}")
        return None
