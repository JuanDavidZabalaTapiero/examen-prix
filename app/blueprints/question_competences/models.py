from app.extensions import db


class QuestionCompetence(db.Model):
    __tablename__ = "question_competences"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
