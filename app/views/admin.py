# requirements: all users, add user, remove user, see transactions of a user
from flask import Blueprint

admin = Blueprint("Admin", __name__, url_prefix="/admin")
