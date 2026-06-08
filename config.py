import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'homeride.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Настройки почты (для Gmail)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # Твой email
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # Пароль приложения
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')