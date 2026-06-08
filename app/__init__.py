from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

login_manager.login_view = 'auth.login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице'

mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Инициализация расширений
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Регистрация blueprint'ов
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.trips import bp as trips_bp
    app.register_blueprint(trips_bp, url_prefix='/')

    from app.bookings import bp as bookings_bp
    app.register_blueprint(bookings_bp, url_prefix='/bookings')
    
    # Загрузка пользователя для Flask-Login
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Главная страница
    @app.route('/')
    def index():
        return '<h1>HomeRide</h1><p>Добро пожаловать!</p>'
    
    return app