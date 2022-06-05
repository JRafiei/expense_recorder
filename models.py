from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ExpenseCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    def __repr__(self):
        return f'<ExpenseCategory {self.name}>'


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime)
    note = db.Column(db.String(200), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey(ExpenseCategory.id), nullable=False)
    category = db.relationship('ExpenseCategory', backref=db.backref('expenses', lazy=True))

    def __repr__(self):
        return f'<Expense {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'value': self.value,
            'note': self.note,
            'timestamp': str(self.timestamp),
            'category': self.category.name
        }