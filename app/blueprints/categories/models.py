from app.extensions import db


class LicenseCategory(db.Model):
    __tablename__ = "license_categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # enrollments
