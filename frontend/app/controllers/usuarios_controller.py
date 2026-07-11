import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from app.config import Config

usuarios_bp = Blueprint('usuarios', __name__)

API_URL = f"{Config.BACKEND_URL}/api/usuarios"
TIMEOUT = 5


@usuarios_bp.route('/')
@login_required
def listar():
    usuarios = []
    try:
        resp = requests.get(API_URL, timeout=TIMEOUT)
        if resp.status_code == 200:
            usuarios = resp.json()
        else:
            flash('El backend respondió con un error al listar usuarios', 'error')
    except requests.exceptions.RequestException:
        flash('No se pudo conectar con el backend', 'error')

    return render_template('usuarios/list.html', usuarios=usuarios)


@usuarios_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def crear():
    if request.method == 'POST':
        data = {
            'nombre': request.form.get('nombre', '').strip(),
            'email': request.form.get('email', '').strip(),
            'telefono': request.form.get('telefono', '').strip(),
        }
        try:
            resp = requests.post(API_URL, json=data, timeout=TIMEOUT)
        except requests.exceptions.RequestException:
            flash('No se pudo conectar con el backend', 'error')
            return render_template('usuarios/form.html', usuario=data, accion='Crear')

        if resp.status_code == 201:
            flash('Usuario creado correctamente', 'success')
            return redirect(url_for('usuarios.listar'))

        error = resp.json().get('error', 'Error al crear usuario') if resp.content else 'Error al crear usuario'
        flash(error, 'error')
        return render_template('usuarios/form.html', usuario=data, accion='Crear')

    return render_template('usuarios/form.html', usuario=None, accion='Crear')


@usuarios_bp.route('/<int:usuario_id>/editar', methods=['GET', 'POST'])
@login_required
def editar(usuario_id):
    if request.method == 'POST':
        data = {
            'nombre': request.form.get('nombre', '').strip(),
            'email': request.form.get('email', '').strip(),
            'telefono': request.form.get('telefono', '').strip(),
        }
        try:
            resp = requests.put(f"{API_URL}/{usuario_id}", json=data, timeout=TIMEOUT)
        except requests.exceptions.RequestException:
            flash('No se pudo conectar con el backend', 'error')
            return render_template('usuarios/form.html', usuario={**data, 'id': usuario_id}, accion='Editar')

        if resp.status_code == 200:
            flash('Usuario actualizado correctamente', 'success')
            return redirect(url_for('usuarios.listar'))

        error = resp.json().get('error', 'Error al actualizar usuario') if resp.content else 'Error al actualizar usuario'
        flash(error, 'error')
        return render_template('usuarios/form.html', usuario={**data, 'id': usuario_id}, accion='Editar')

    try:
        resp = requests.get(f"{API_URL}/{usuario_id}", timeout=TIMEOUT)
    except requests.exceptions.RequestException:
        flash('No se pudo conectar con el backend', 'error')
        return redirect(url_for('usuarios.listar'))

    if resp.status_code != 200:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('usuarios.listar'))

    return render_template('usuarios/form.html', usuario=resp.json(), accion='Editar')


@usuarios_bp.route('/<int:usuario_id>/eliminar', methods=['POST'])
@login_required
def eliminar(usuario_id):
    try:
        resp = requests.delete(f"{API_URL}/{usuario_id}", timeout=TIMEOUT)
    except requests.exceptions.RequestException:
        flash('No se pudo conectar con el backend', 'error')
        return redirect(url_for('usuarios.listar'))

    if resp.status_code == 200:
        flash('Usuario eliminado correctamente', 'success')
    else:
        flash('No se pudo eliminar el usuario', 'error')

    return redirect(url_for('usuarios.listar'))
