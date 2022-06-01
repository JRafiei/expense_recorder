from crypt import methods
import os
from flask import Flask, request
from models import db, Expense, ExpenseCategory
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.getcwd()}/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# with app.app_context():
#     db.create_all()


def add_category():
    cat_name = request.json.get('cat')
    cat = ExpenseCategory(name=cat_name)
    try:
        db.session.add(cat)
        db.session.commit()
    except IntegrityError as e:
        return {"status": "error", "reason": "category_already_exists"}

    return {"status": "success"}


def add_expense():
    try:
        title = request.json.get('title')
        value = request.json.get('value')
        cat_name = request.json.get('cat')
        cat = db.session.query(ExpenseCategory).filter(ExpenseCategory.name==cat_name).first()
        if cat is None:
            return {"status": "error", "reason": "category_does_not_exists"}

        expense = Expense(title=title, value=value, category=cat)
        cat.expenses.append(expense)
        db.session.commit()
    except Exception as e:
        return {"status": "error", "reason": type(e).__name__}
    return {"status": "success"}


app.add_url_rule("/add-category", view_func=add_category, methods=['POST'])
app.add_url_rule("/add-expense", view_func=add_expense, methods=['POST'])
