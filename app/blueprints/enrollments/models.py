from app.extensions import db


class Enrollment(db.Column):
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey("license_categories.id"), nullable=False
    )
