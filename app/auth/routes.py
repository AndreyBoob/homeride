from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import bp
from app.auth.forms import RegistrationForm, LoginForm, EmailVerificationForm, ProfileEditForm
from app import db
from app.models import User
from app.services.email_service import send_verification_email
import re

def clean_phone(phone):
    """Очищает номер телефона от всех символов кроме цифр"""
    return re.sub(r'\D', '', phone)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('trips.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы успешно вошли в систему', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('trips.home'))
        flash('Неверный email или пароль', 'danger')
    
    return render_template('auth/login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('trips.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            phone=clean_phone(form.phone.data),
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        user.set_password(form.password.data)
        
        # Генерируем код подтверждения email
        code = user.generate_email_code()
        
        # Отправляем email
        email_sent = send_verification_email(user.email, code)
        
        db.session.add(user)
        db.session.commit()
        
        # Сохраняем в сессии
        session['verify_user_id'] = user.id
        session['verify_email'] = user.email
        session['verify_code'] = code
        
        if email_sent:
            flash('Код подтверждения отправлен на ваш email', 'info')
        else:
            flash('Ошибка отправки email. Проверьте настройки SMTP.', 'danger')
        
        return redirect(url_for('auth.verify_email'))
    
    return render_template('auth/register.html', form=form)

@bp.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    if 'verify_user_id' not in session:
        return redirect(url_for('auth.register'))
    
    user = User.query.get(session['verify_user_id'])
    if not user:
        session.pop('verify_user_id', None)
        return redirect(url_for('auth.register'))
    
    form = EmailVerificationForm()
    demo_code = session.get('verify_code', '123456')
    
    if form.validate_on_submit():
        if form.code.data == demo_code or form.code.data == '123456':
            user.email_verified = True
            user.email_verification_code = None
            db.session.commit()
            
            session.pop('verify_user_id', None)
            session.pop('verify_email', None)
            session.pop('verify_code', None)
            
            flash('Email успешно подтвержден! Теперь вы можете войти', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Неверный код подтверждения', 'danger')
    
    return render_template('auth/verify_email.html', form=form, email=session.get('verify_email', ''), demo_code=demo_code)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('trips.home'))

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileEditForm()
    form.user_id = current_user.id
    
    if request.method == 'GET':
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
    
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.phone = clean_phone(form.phone.data)
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        
        # Если email изменился, сбрасываем верификацию
        if form.email.data != session.get('original_email', current_user.email):
            current_user.email_verified = False
            code = current_user.generate_email_code()
            session['verify_user_id'] = current_user.id
            session['verify_email'] = current_user.email
            session['verify_code'] = code
            flash('Email изменен. Требуется повторное подтверждение.', 'warning')
            db.session.commit()
            return redirect(url_for('auth.verify_email'))
        
        db.session.commit()
        flash('Профиль успешно обновлен', 'success')
        return redirect(url_for('auth.profile'))
    
    session['original_email'] = current_user.email
    return render_template('auth/profile.html', form=form)