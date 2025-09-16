from app.extensions import db


class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey("license_categories.id"), nullable=False
    )

    category = db.relationship("LicenseCategory", backref="enrollments")
    student = db.relationship("Student", back_populates="enrollments")
