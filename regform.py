from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email


class RegForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(), Length(3, 15)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(6, 25,
                                                                          message="Длина пароля должна быть "
                                                                                  "от 6 до 25 символов")])
    password_validate = PasswordField('Пароль', validators=[DataRequired(), Length(6, 25,
                                                                                 message="Длина пароля должна быть "
                                                                                 "от 6 до 25 символов")])
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    patronymic = StringField('Patronymic', validators=[DataRequired()])
    submit = SubmitField('Cоздать аккаунт')
