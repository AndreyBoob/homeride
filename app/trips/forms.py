from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, IntegerField, FloatField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class TripForm(FlaskForm):
    from_location = StringField('Откуда', validators=[DataRequired(), Length(max=255)])
    to_location = StringField('Куда', validators=[DataRequired(), Length(max=255)])
    departure_date = DateField('Дата отправления', validators=[DataRequired()])
    departure_time = TimeField('Время отправления')
    available_seats = IntegerField('Количество мест', validators=[DataRequired(), NumberRange(min=1, max=10)])
    price = FloatField('Цена за место (₽)', validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField('Описание поездки')
    submit = SubmitField('Создать поездку')