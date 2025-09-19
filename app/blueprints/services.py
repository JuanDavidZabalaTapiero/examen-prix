from sqlalchemy import case, func

from app.extensions import db

from .document_types.models import DocumentType
from .question_competences.models import QuestionCompetence
from .questions.models import Option, Question, QuestionCompetenceAssociation
from .students.models import Response, Student
from .students.services import get_student

# == CREATE ==


# == READ ==
def get_scores():
    try:
        query = (
            db.session.query(
                Student.id.label("student_id"),
                Student.name.label("student_name"),
                Student.doc_number,
                DocumentType.name.label("document_name"),
                QuestionCompetence.name.label("competence_name"),
                func.count(Response.id).label("total_respuestas"),
                func.sum(case((Option.is_correct, 1), else_=0)).label(
                    "respuestas_correctas"
                ),
            )
            .join(Response, Student.id == Response.student_id)
            .join(Option, Response.option_id == Option.id)
            .join(Question, Option.question_id == Question.id)
            .join(
                QuestionCompetenceAssociation,
                Question.id == QuestionCompetenceAssociation.question_id,
            )
            .join(
                QuestionCompetence,
                QuestionCompetenceAssociation.question_competence_id
                == QuestionCompetence.id,
            )
            .join(DocumentType, Student.doc_type_id == DocumentType.id)
            .group_by(Student.id, DocumentType.name, QuestionCompetence.name)
            .all()
        )

        results = {}

        for (
            student_id,
            student_name,
            doc_number,
            doc_name,
            competence_name,
            total,
            correct,
        ) in query:
            percentage = (correct / total * 100) if total > 0 else 0

            if student_id not in results:
                results[student_id] = {
                    "id": student_id,
                    "name": student_name,
                    "doc_number": doc_number,
                    "document": doc_name,
                    "competence_percentages": {},  # aquí van por competencia
                    "total_percentage": 0,
                    "categories": [],
                }

            results[student_id]["competence_percentages"][competence_name] = round(
                percentage, 2
            )

        # AGREGAR CATEGORÍAS
        for item in results.values():
            student_id = item["id"]
            ok, msg, student = get_student(student_id)

            if ok:
                item["categories"] = [en.category.name for en in student.enrollments]
                comps = item["competence_percentages"].values()
                item["total_percentage"] = (
                    round(sum(comps) / len(comps), 2) if comps else 0
                )
            else:
                item["categories"] = []
                return {"success": False, "message": msg, "data": results}

        return {
            "success": True,
            "message": "Estudiantes y porcentajes obtenidos correctamente",
            "data": list(results.values()),
        }

    except Exception as e:
        print(f"Error en get_score: {e}")
        return {
            "success": False,
            "message": "Error interno al consultar los estudiantes y porcentajes",
            "data": [],
        }


# == UPDATE ==

# == DELETE ==
