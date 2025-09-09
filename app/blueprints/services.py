from sqlalchemy import case, func

from app.extensions import db

from .questions.models import Option
from .students.models import Response, Student


def get_students_with_scores():
    try:
        query = (
            db.session.query(
                Student.id,
                Student.name,
                func.count(Response.id).label("total_respuestas"),
                func.sum(case((Option.is_correct, 1), else_=0)).label(
                    "respuestas_correctas"
                ),
            )
            .join(Response, Student.id == Response.student_id)
            .join(Option, Response.option_id == Option.id)
            .group_by(Student.id)
            .all()
        )

        results = []
        for student_id, name, total, correct_answers in query:
            percentage = (correct_answers / total * 100) if total > 0 else 0
            results.append(
                {"id": student_id, "name": name, "percentage": round(percentage, 2)}
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
