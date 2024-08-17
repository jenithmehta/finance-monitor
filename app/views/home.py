from flask import (
    Blueprint,
    Response,
    flash,
    redirect,
    render_template,
    request,
    stream_with_context,
    url_for,
)
from sqlalchemy import func

from app.db import Statements, User, db

# from app.forms import NewStatementForm, StatementEditForm
# from app.functions import generate_string
from app.utils import get_current_user, get_current_user_balance, user_login_required

home = Blueprint("Home", __name__)


@home.route("/")
@user_login_required
def home_index():
    user = get_current_user()
    user_details = {}
    user_details["name"] = user.name
    user_details["account_balance"] = round(get_current_user_balance(), 2)
    statements = (
        db.session.query(Statements)
        .filter(Statements.user_id == 1)
        .order_by(Statements.operation_time.desc())
        .limit(5)
        .all()
    )
    user_details["statements"] = [
        {
            "desc": res.description,
            "amount": res.amount,
            "at": res.operation_time,
            "id": res.statement_id,
        }
        for res in statements
    ]
    return render_template("home/index.html", user=user_details)


@home.route("/new", methods=("GET", "POST"))
@user_login_required
def new_statement():
    form = NewStatementForm(request.form)
    if form.validate_on_submit():
        amount = form.amount.data
        description = form.description.data
        at = form.datetime_data.data
        income = form.income.data
        expense = form.expense.data

        if not income and not expense:
            flash("Cannot add statement that is neither income nor expense!", "red")
            return redirect(url_for(".new_statement"))

        amount = abs(amount)
        if expense is True:
            amount = -amount

        current_user = get_current_user()
        user_id = current_user.id

        statement = Statements(
            description=description,
            amount=amount,
            operation_time=at,
            user_id=user_id,
            statement_id=generate_string(),
        )

        db.session.add(statement)
        db.session.commit()

        flash("Statement was added to your account successfully.", "green")
        return redirect(url_for("Home.home_index"))

    return render_template("home/new_statement.html", title="New statement", form=form)

