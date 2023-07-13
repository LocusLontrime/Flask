from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email


class Registration(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    surname = StringField(label='Surname', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(label='Confirm password', validators=[DataRequired(), EqualTo('password')])

    def validate_password(self, field):
        if not any(map(str.isdigit, field.data)):
            raise ValidationError("Пароль должен содержать хотя бы одну цифру")
        if not any(map(str.isalpha, field.data)):
            raise ValidationError("Пароль должен содержать хотя бы одну букву")