from flask_mail import Message
from flask import current_app
from app import mail

def send_verification_email(email, code):
    """Отправляет код подтверждения на email"""
    try:
        msg = Message(
            subject='HomeRide - Код подтверждения',
            recipients=[email],
            html=f"""
            <h2>Добро пожаловать в HomeRide!</h2>
            <p>Ваш код подтверждения: <strong style="font-size: 24px; color: #4299e1;">{code}</strong></p>
            <p>Введите этот код на странице подтверждения.</p>
            <p>Если вы не регистрировались в HomeRide, просто проигнорируйте это письмо.</p>
            <hr>
            <p><small>HomeRide - сервис поиска попутчиков</small></p>
            """
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Ошибка отправки email: {e}")
        return False