from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class EncryptForm(FlaskForm):
    word = StringField("Введите слово", validators=[DataRequired()])
    select = SelectField("Выберите режим", choices=['Закодировать', "Раскодировать"])
    submit = SubmitField("Готово")