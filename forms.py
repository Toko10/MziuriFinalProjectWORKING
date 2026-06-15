from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, IntegerField, SubmitField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, equal_to, length, ValidationError
from models import User

class RegisterForm(FlaskForm):
    username = StringField("Enter Username", validators=[
        DataRequired(),
        length(min=4, max=20, message="იუზერნეიმი უნდა იყოს 4-დან 20 სიმბოლომდე")
    ])
    password = PasswordField("Enter Password", validators=[
        DataRequired(),
        length(min=6, max=24, message="პაროლი უნდა იყოს 6-დან 24 სიმბოლომდე"),
    ])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(),
        equal_to("password", message="პაროლები არ ემთხვევა")
    ])

    register = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("ეს მომხმარებლის სახელი უკვე დაკავებულია!")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    login = SubmitField("Log In")


class ArtistForm(FlaskForm):
    name = StringField("Artist Name", validators=[DataRequired()])
    debut_year = IntegerField("Debut Year", validators=[DataRequired()])
    image = FileField("Artist Image")
    submit = SubmitField("Save Artist")

class ReviewForm(FlaskForm):
    text = StringField("Drop your comment here", validators=[DataRequired()])
    submit = SubmitField("Post Review")