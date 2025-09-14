from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db

from .models import Response, Student


def register_student(name, doc_type_id, doc_number):
    if not name or not doc_type_id or not doc_number:
        return False, "Todos los campos son obligatorios", None

    try:
        new_student = Student(name=name, doc_type_id=doc_type_id, doc_number=doc_number)
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
