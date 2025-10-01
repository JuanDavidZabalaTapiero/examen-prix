from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db

from .models import Response, Student


# == CREATE ==
def register_student(name, doc_type_id, doc_number):
    if not name or not doc_type_id or not doc_number:
        return False, "Todos los campos son obligatorios", None

    name = name.strip()
    doc_type_id = doc_type_id.strip()
    doc_number = doc_number.strip()

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


# == READ ==
def get_student(student_id):
    if not student_id:
        return False, "Campos obligatorios", None

    try:
        student = Student.query.get(student_id)

        if not student:
            return False, "El alumno no existe", None

        return True, "Alumno consultado correctamente", student

    except Exception as e:
        print(f"Error en get_student: {e}")
        return False, "Error al intentar consultar el alumno", None


# == UPDATE ==

# == DELETE
