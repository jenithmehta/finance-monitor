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
