from sqlalchemy import case, func

from app.extensions import db

from .document_types.models import DocumentType
from .questions.models import Option
from .students.models import Response, Student

# == CREATE ==


# == READ ==
def get_students_with_scores():
    try:
        query = (
            db.session.query(Student)
            .join(Response, Student.id == Response.student_id)
            .join(Option, Response.option_id == Option.id)
            .join(DocumentType, Student.doc_type_id == DocumentType.id)
            .group_by(Student.id, DocumentType.name)
            .add_columns(
                DocumentType.name.label("document_name"),
                func.count(Response.id).label("total_respuestas"),
                func.sum(case((Option.is_correct, 1), else_=0)).label(
                    "respuestas_correctas"
                ),
            )
            .all()
        )

        results = []

        for student, document_name, total, correct_answers in query:

            percentage = (correct_answers / total * 100) if total > 0 else 0

            results.append(
                {
                    "id": student.id,
                    "name": student.name,
                    "doc_number": student.doc_number,
                    "document": document_name,
                    "percentage": round(percentage, 2),
                    "categories": [en.category.name for en in student.enrollments]
                    or ["Sin categorías asociadas"],
                }
            )

        return {
            "success": True,
            "message": "Alumnos y porcentajes obtenidos correctamente",
            "data": results,
        }

    except Exception as e:
        print(f"Error al intentar consultar los alumnos y sus porcentajes: {e}")
        return {
            "success": False,
            "message": "Error interno al consultar los estudiantes y porcentajes",
            "data": [],
        }


# == UPDATE ==

# == DELETE ==
