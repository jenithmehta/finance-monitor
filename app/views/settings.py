from flask import Blueprint

from app.utils import user_login_required

settings = Blueprint("Settings", __name__, url_prefix="/settings")


@settings.route("/")
@user_login_required
def settings_index():
    return 200
