import os
from flask import Flask
from models import db, Expense, ExpenseCategory


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.getcwd()}/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


with app.app_context():
    db.create_all()
    cat = ExpenseCategory(name='clothes')
    expense1 = Expense(title='taj', value=1100, category=cat)
    cat.expenses.append(expense1)
    db.session.add(cat)
    db.session.commit()
