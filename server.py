from crypt import methods
import os
from datetime import datetime
from flask import Flask, request, render_template
from models import db, Expense, ExpenseCategory
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.getcwd()}/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# with app.app_context():
#     db.create_all()


def home():
    now = datetime.now()
    year = now.year
    month_name = now.strftime('%B')
    categories = db.session.query(ExpenseCategory).all()
    last_expenses = db.session.query(Expense).order_by(Expense.id.desc()).limit(5)
    data = {
        'categories': categories,
        'expenses': last_expenses,
        'year': year,
        'month_name': month_name
    }
    return render_template('home.html', **data)


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


def get_category_expenses():
    if request.data:
        cat_name = request.json.get('cat')
        if cat_name:
            cat = db.session.query(ExpenseCategory).filter(ExpenseCategory.name==cat_name).first()
            expenses = db.session.query(Expense).filter(Expense.category_id==cat.id).all()
        else:
            return {"status": "error", "reason": "category_is_not_provided"}
    else:
        expenses = db.session.query(Expense).all()

    expenses = [expense.to_dict() for expense in expenses]
    return {"status": "success", "expenses": expenses}


def get_range_expenses():
    try:
        start_time = datetime.strptime(request.json.get('stime'), '%Y-%m-%d %H:%M:%S')
    except:
        return {"status": "error", "reason": "wrong_start_time"}

    try:
        end_time = datetime.strptime(request.json.get('etime'), '%Y-%m-%d %H:%M:%S')
    except:
        end_time = datetime.now()

    expenses = db.session.query(Expense).filter(Expense.timestamp.between(start_time, end_time)).all()
    expenses = [expense.to_dict() for expense in expenses]
    return {"status": "success", "expenses": expenses}


app.add_url_rule("/", view_func=home, methods=['GET'])
app.add_url_rule("/add-category", view_func=add_category, methods=['POST'])
app.add_url_rule("/add-expense", view_func=add_expense, methods=['POST'])
app.add_url_rule("/get-expenses", view_func=get_category_expenses, methods=['GET'])
app.add_url_rule("/get-range-expenses", view_func=get_range_expenses, methods=['GET'])
