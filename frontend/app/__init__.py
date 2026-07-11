from flask import Flask, redirect, url_for
from flask_login import LoginManager

from app.config import Config
from app.auth import AdminUser

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Debes iniciar sesión para acceder'
    login_manager.login_message_category = 'error'

    @login_manager.user_loader
    def load_user(user_id):
        if user_id == Config.ADMIN_USERNAME:
            return AdminUser(user_id)
        return None

    from app.controllers.auth_controller import auth_bp
    from app.controllers.usuarios_controller import usuarios_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')

    @app.route('/')
    def index():
        return redirect(url_for('usuarios.listar'))

    return app
