from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class BooksForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    letter = SelectField(u'Буква класса', choices=[('А', 'А'), ('Б', 'Б'), ('В', 'В'), ('Г', 'Г'), ('Общая', 'Общая')])
    submit = SubmitField('Применить')