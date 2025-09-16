from sqlalchemy import func

from app.extensions import db


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    doc_type_id = db.Column(
        db.Integer, db.ForeignKey("document_types.id"), nullable=False
    )
    doc_number = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)

    # RELATIONSHIPS
    responses = db.relationship(
        "Response", backref="student", cascade="all, delete-orphan"
    )
    document = db.relationship("DocumentType", back_populates="students", lazy="joined")
    enrollments = db.relationship("Enrollment", back_populates="student")


class Response(db.Model):
    __tablename__ = "responses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey("options.id"), nullable=False)

    # student

    # option
