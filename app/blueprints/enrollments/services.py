from app.extensions import db

from .models import Enrollment


# == CREATE ==
def create_enrollment_service(student_id, category_id):
    if not student_id or not category_id:
        return False, "Todos los campos son obligatorios", None

    try:
        enrollment = Enrollment(student_id=student_id, category_id=category_id)
        db.session.add(enrollment)
        db.session.commit()
        return True, "Matricula registrada correctamente", enrollment
    except Exception as e:
        db.session.rollback()
        print(f"Error en create_enrollment_service: {e}")
        return False, "Error al intentar registrar las categorías", None


# == READ ==

# == UPDATE ==

# == DELETE ==
