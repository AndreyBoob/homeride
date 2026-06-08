from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Номер телефона', validators=[DataRequired(), Length(min=10, max=20)])
    first_name = StringField('Имя', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Фамилия', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Подтвердите пароль', 
                                      validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот email уже зарегистрирован')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class EmailVerificationForm(FlaskForm):
    code = StringField('Код подтверждения', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Подтвердить')

class ProfileEditForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Номер телефона', validators=[DataRequired(), Length(min=10, max=20)])
    first_name = StringField('Имя', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Фамилия', validators=[DataRequired(), Length(max=64)])
    submit = SubmitField('Сохранить изменения')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and user.id != self.user_id:
            raise ValidationError('Этот email уже используется')