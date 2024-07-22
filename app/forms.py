# a form is required to accept
# email, password, submit button
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class AuthForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=(
            DataRequired("Email is required"),
            Email("Please enter valid email"),
        ),
    )
    password = PasswordField(
        "Passowrd",
        validators=[
            DataRequired("Password field can't be empty"),
            Length(min=8, message="Password length should be minium 8 characters"),
        ],
    )
    submit = SubmitField("Submit")
