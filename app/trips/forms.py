from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, IntegerField, FloatField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class TripForm(FlaskForm):
    # Откуда
    from_city = StringField('Город (откуда)', validators=[DataRequired(), Length(max=100)])
    from_street = StringField('Улица (откуда)', validators=[Length(max=200)])
    from_house = StringField('Дом (откуда)', validators=[Length(max=20)])
    from_entrance = StringField('Подъезд (откуда)', validators=[Length(max=10)])
    
    # Куда
    to_city = StringField('Город (куда)', validators=[DataRequired(), Length(max=100)])
    to_street = StringField('Улица (куда)', validators=[Length(max=200)])
    to_house = StringField('Дом (куда)', validators=[Length(max=20)])
    to_entrance = StringField('Подъезд (куда)', validators=[Length(max=10)])
    
    # Остальные поля
    departure_date = DateField('Дата отправления', validators=[DataRequired()])
    departure_time = TimeField('Время отправления')
    available_seats = IntegerField('Количество мест', validators=[DataRequired(), NumberRange(min=1, max=10)])
    price = FloatField('Цена за место (₽)', validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField('Описание поездки')
    submit = SubmitField('Создать поездку')