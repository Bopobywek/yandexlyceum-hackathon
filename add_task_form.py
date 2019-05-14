from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, TimeField
from wtforms.validators import DataRequired


class AddTaskForm(FlaskForm):
    title = StringField('Название задачи', validators=[DataRequired()])
    content = TextAreaField('Описание задачи', validators=[DataRequired()])
    deadline = StringField('Дата выполнения задачи', validators=[DataRequired()])
    submit = SubmitField('Добавить')
