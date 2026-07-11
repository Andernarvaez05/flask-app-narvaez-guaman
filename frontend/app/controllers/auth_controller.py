from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash

from app.config import Config
from app.auth import AdminUser

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        credenciales_validas = (
            username == Config.ADMIN_USERNAME
            and Config.ADMIN_PASSWORD_HASH
            and check_password_hash(Config.ADMIN_PASSWORD_HASH, password)
        )

        if credenciales_validas:
            login_user(AdminUser(username))
            siguiente = request.args.get('next')
            return redirect(siguiente or url_for('usuarios.listar'))

        flash('Usuario o contraseña incorrectos', 'error')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('auth.login'))
