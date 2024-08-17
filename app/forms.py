# a form is required to accept
# email, password, submit button
from flask_wtf import FlaskForm
from wtforms import (
    DateTimeLocalField,
    EmailField,
    FloatField,
    PasswordField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, Length, NumberRange


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


class NewStatementForm(FlaskForm):
    amount = FloatField(
        "Enter amount",
        [
            DataRequired("Amount is required!"),
            NumberRange(
                0.0001,
                9999999999.99,
                "Entered amount could not be added to your statement!",
            ),
        ],
    )
    description = TextAreaField(
        "Enter description",
        [
            DataRequired("Description is required!"),
            Length(5, 180, "Description can contain 5 to 180 characters!"),
        ],
        render_kw={"class": "textarea-h", "rows": "2"},
    )

    datetime_data = DateTimeLocalField(
        format="%Y-%m-%dT%H:%M", validators=[DataRequired("This field is required!")]
    )

    expense = SubmitField("Add Expense")
    income = SubmitField("Add Income")
