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
    return user
