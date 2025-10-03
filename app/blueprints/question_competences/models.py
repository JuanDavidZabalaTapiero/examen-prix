from app.extensions import db


class QuestionCompetence(db.Model):
    __tablename__ = "question_competences"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    parent_id = db.Column(
        db.Integer, db.ForeignKey("question_competences.id"), nullable=True
    )

    parent = db.relationship(
        "QuestionCompetence", remote_side=[id], backref="subcompetences"
    )

    def to_dict(self):
        return {"id": self.id, "name": self.name}
