from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import User, db
from app.forms import AuthForm
from app.utils import (
    generate_id,
    get_base64_encode,
    is_user_loggedin,
    user_login_required,
)

# TODO: add signup page

auth = Blueprint("Auth", __name__, url_prefix="/auth")


@auth.route("/", methods=("GET", "POST"))
def auth_index():
    if is_user_loggedin() is True:
        return redirect(url_for("Home.home_index"))

    form = AuthForm(request.form)

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        data = User.query.filter(User.email == email).first()

        if data:
            print(data.password)
            print(generate_password_hash(password))
            if check_password_hash(data.password, password) is True:
                session.permanent = True
                session["session-sign-id"] = get_base64_encode(data.session_id)
                return redirect(url_for("Home.home_index"))
            else:
                flash("Incorrect password for entered email account!", "red")
        else:
            # hashed_password = generate_password_hash(password, method="SHA256")
            hashed_password = generate_password_hash(password)
            name = email.split("@")[0][:18]
            user = User(  # type: ignore
                name=name,
                email=email,
                password=hashed_password,
                session_id=generate_id(name, email, hashed_password),
            )

            db.session.add(user)
            db.session.commit()

            flash("New account has been created, enter credentials to signin.", "green")

        return redirect(url_for(".auth_index"))

    return render_template("auth/index.html", title="Login", form=form)


@auth.route("/logout", methods=["GET", "POST"])
@user_login_required
def logout():
    if "session-sign-id" in session:
        session.pop("session-sign-id")
    session.permanent = False
    return redirect(url_for(".auth_index"))
