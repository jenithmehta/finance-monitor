import base64
import datetime
import hashlib
import logging
import random
import traceback
import typing as t
import uuid
from functools import wraps

from flask import redirect, session, url_for
from sqlalchemy import func

from app.db import Statements, User


def is_user_loggedin():
    login = False
    sessionid: str = session.get("session-sign-id", "")
    if sessionid:
        # decode
        sessionid_decode = decodebase64(sessionid)
        # query database
        if sessionid_decode:
            if sessionid_decode and sessionid_decode != "":
                user = User.query.filter(User.session_id == sessionid_decode).first()
                if user:
                    login = True
                session.pop("session-sign-id")
        return login


def decodebase64(buffer: str):
    "decode base64"
    try:
        val = base64.b64decode(buffer).decode()
    except Exception as err:
        logging.error(f"exception occured: {err}\ntraceback: {traceback.format_exc()}")
        val = ""
    return val


def get_base64_encode(buffer: str):
    try:
        val = buffer.encode()
    except Exception as err:
        logging.error(f"exception occured: {err}\ntraceback: {traceback.format_exc()}")
        val = "".encode()
    return base64.urlsafe_b64encode(val).decode()


def generate_id(name: str, email: str, hashed_password: str, limit: int = 16):
    req = "--".join(
        [
            name,
            email,
            hashed_password,
            str(datetime.datetime.now(tz=datetime.timezone.utc)),
        ]
    )
    req += uuid.uuid4().hex
    return hashlib.sha1(
        "".join(random.choice(req) for _ in range(limit)).encode()
    ).hexdigest()


def user_login_required(f):  # type:ignore
    """decorator to check login"""

    @wraps(f)
    def fun(*args, **kwargs):  # type:ignore
        if is_user_loggedin() is True:
            return f(*args, **kwargs)  # type: ignore
        return redirect(url_for("Auth.auth_index"))

    return fun  # type: ignore


def admin_login_required(f):  # type:ignore
    """admin login decorator"""

    @wraps(f)
    def fun(*args, **kwargs):  # type:ignore
        if "admin-sign-id" in session:
            return f(*args, **kwargs)  # type:ignore
        return redirect(url_for("Admin.admin_login"))

    return fun  # type:ignore


def get_current_user():
    session_idbase64 = session.get("session-sign-id", "")
    session_id = decodebase64(session_idbase64)
    user_details = User.query.filter(User.session_id == session_id).first_or_404(
        "User not found"
    )
    return user_details


def get_current_user_balance():
    user_id = get_current_user().id
    balance = (
        Statements.query.with_entities(func.sum(Statements.amount))
        .filter(Statements.user_id == user_id)
        .first()[0]  # type: ignore
    )
    return balance if balance else 0.0
