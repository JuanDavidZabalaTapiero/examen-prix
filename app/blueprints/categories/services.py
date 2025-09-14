from sqlalchemy.exc import IntegrityError

from app.extensions import db

from .models import LicenseCategory


# == CREATE ==
def create_category_service(name):
    if not name:
        return False, "Todos los campos son obligatorios", None
    try:
        category = LicenseCategory(name=name)
        db.session.add(category)
        db.session.commit()
        return True, "Categoría registrada correctamente", category
    except IntegrityError:
        db.session.rollback()
        return False, f"La categoría {name} ya está registrada", None
    except Exception as e:
        db.session.rollback()
        print(f"Error en create_category: {e}")
        return False, "Error al intentar registrar la categoría", None


# == READ ==
def get_all_categories():
    try:
        categories = LicenseCategory.query.all()
        return True, "Categorías consultadas correctamente", categories
    except Exception as e:
        print(f"Error en get_all_categories: {e}")
        return False, "Error al intentar consultar las categorías", []


def get_category(category_id):
    try:
        category = LicenseCategory.query.get(category_id)
        return True, "Categoría consultada correctamente", category
    except Exception as e:
        print(f"Error en get_category: {e}")
        return False, "Error al intentar consultar la categoría", None


# == UPDATE ==
def update_category_service(category_id, name):
    if not category_id or not name:
        return False, "Todos los campos son obligatorios", None
    try:
        success, message, category = get_category(category_id)
        if not success:
            return False, message, None

        category.name = name
        db.session.commit()
        return True, "Categoría editada", category

    except Exception as e:
        db.session.rollback()
        print(f"Error en update_category_service: {e}")
        return False, "Error al intentar editar la categoría", None


# == DELETE ==
def delete_category_service(category_id):
    if not category_id:
        return False, "Todos los campos son obligatorios"
    try:
        success, message, category = get_category(category_id)

        if not success:
            return False, message

        if category.enrollments:
            return False, "La categoría está vinculada a una o varías matriculas"

        db.session.delete(category)
        db.session.commit()
        return True, "Categoría eliminada"

    except Exception as e:
        db.session.rollback()
        print(f"Error en delete_category_service: {e}")
        return False, "Error al intentar eliminar la categoría"
