import calendar
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


def add_expense_view():
    categories = db.session.query(ExpenseCategory).all()
    data = {
        'categories': categories,
    }
    return render_template('add_expense.html', **data)


def get_monthly_expenses():
    year = int(request.args.get('year'))
    month = request.args.get('month')
    month_number = datetime.strptime(month, "%B").month
    last_month_day = calendar.monthrange(year, month_number)[1]
    start_time = datetime(year=year, month=month_number, day=1, hour=0, minute=0, second=0)
    end_time = datetime(year=year, month=month_number, day=last_month_day, hour=0, minute=0, second=0)
    expenses = db.session.query(Expense).filter(Expense.timestamp.between(start_time, end_time))
    expenses = expenses.order_by(Expense.timestamp.desc())
    day_expenses = {}
    category_expenses = {}
    for expense in expenses:
        key = expense.timestamp.strftime('%Y-%m-%d')
        if key not in day_expenses:
            day_expenses[key] = {'expenses': [], 'total': 0}
        day_expenses[key]['expenses'].append(expense)
        day_expenses[key]['total'] += expense.value

        key2 = expense.category.name
        if key2 not in category_expenses:
            category_expenses[key2] = 0
        category_expenses[key2] += expense.value
        
    data = {
        "day_expenses": day_expenses,
        "category_expenses": category_expenses,
        "month_name": month,
        "year": year
    }
    return render_template('monthly_expenses.html', **data)


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
        timestamp = request.json.get('timestamp')
        if timestamp:
            timestamp = datetime.strptime(request.json['timestamp'], '%Y-%m-%dT%H:%M')
        else:
            timestamp = datetime.now()

        cat = db.session.query(ExpenseCategory).filter(ExpenseCategory.name==cat_name).first()
        if cat is None:
            return {"status": "error", "reason": "category_does_not_exists"}

        expense = Expense(title=title, value=value, category=cat, timestamp=timestamp)
        cat.expenses.append(expense)
        db.session.commit()
    except Exception as e:
        return {"status": "error", "reason": type(e).__name__}
    return {"status": "success"}


def get_category_expenses():
    cat_name = request.args.get('cat')
    if cat_name:
        cat = db.session.query(ExpenseCategory).filter(ExpenseCategory.name==cat_name).first()
        if cat is None:
            return {"status": "error", "reason": "category_does_not_exists"}
        else:
            expenses = db.session.query(Expense).filter(Expense.category_id==cat.id)
    else:
        expenses = db.session.query(Expense)

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

    expenses = db.session.query(Expense).filter(Expense.timestamp.between(start_time, end_time))
    expenses = [expense.to_dict() for expense in expenses]
    return {"status": "success", "expenses": expenses}


app.add_url_rule("/", view_func=home, methods=['GET'])
app.add_url_rule("/add", view_func=add_expense_view, methods=['GET'])
app.add_url_rule("/monthly-expenses", view_func=get_monthly_expenses, methods=['GET'])
app.add_url_rule("/add-category", view_func=add_category, methods=['POST'])
app.add_url_rule("/add-expense", view_func=add_expense, methods=['POST'])
app.add_url_rule("/get-expenses", view_func=get_category_expenses, methods=['GET'])
app.add_url_rule("/get-range-expenses", view_func=get_range_expenses, methods=['GET'])
