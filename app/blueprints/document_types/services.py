from sqlalchemy.exc import IntegrityError

from app.extensions import db

from .models import DocumentType


# == CREATE ==
def create_document_type_service(name):
    if not name:
        return False, "Todos los campos son obligatorios", None
    try:
        doc_type = DocumentType(name=name)
        db.session.add(doc_type)
        db.session.commit()
        return True, "Tipo de documento registrado correctamente", doc_type

    except IntegrityError:
        db.session.rollback()
        return False, "El tipo de documento ya está registrado", None

    except Exception as e:
        db.session.rollback()
        print(f"Error en create_document_type_service: {e}")
        return False, "Error al intentar registrar el tipo de documento", None


# == READ ==
def get_all_document_types():
    try:
        document_types = DocumentType.query.all()
        return True, "Tipos de documento consultados correctamente", document_types
    except Exception as e:
        print(f"Error en get_all_document_types: {e}")
        return False, "Error al intentar consultar los tipos de documento", []


def get_document_type(document_type_id):
    if not document_type_id:
        return False, "Todos los campos son obligatorios", None
    try:
        document_type = DocumentType.query.get(document_type_id)
        return True, "Tipo de documento consultado correctamente", document_type
    except Exception as e:
        print(f"Error en get_document_type: {e}")
        return False, "Error al intentar consultar el tipo de documento", None


# == UPDATE ==
def update_document_type_service(document_type_id, name):
    if not document_type_id or not name:
        return False, "Todos los campos son obligatorios", None
    try:
        success, message, document_type = get_document_type(document_type_id)

        if not success:
            return False, message

        document_type.name = name
        db.session.commit()

        return True, "Tipo de documento editado", document_type

    except Exception as e:
        db.session.rollback()
        print(f"Error en update_document_type_service: {e}")
        return False, "Error al intentar editar el tipo de documento", None


# == DELETE ==
def delete_document_type_service(document_type_id):
    if not document_type_id:
        return False, "Todos los campos son obligatorios"

    try:
        success, message, document_type = get_document_type(document_type_id)

        if not success:
            return False, message

        if document_type.students:
            return False, "Hay alumnos registrados con este tipo de documento"

        db.session.delete(document_type)
        db.session.commit()

        return True, "Tipo de documento eliminado"

    except Exception as e:
        db.session.rollback()
        print(f"Error en delete_document_type: {e}")
        return False, "Error al intentar eliminar el tipo de documento"
