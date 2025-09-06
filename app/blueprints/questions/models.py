from app.extensions import db


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    text = db.Column(db.String(255), nullable=False)

    options = db.relationship(
        "Option", backref="question", cascade="all, delete-orphan"
    )


class Option(db.Model):
    __tablename__ = "options"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)

    responses = db.relationship(
        "Response", backref="option", cascade="all, delete-orphan"
    )

    # question
