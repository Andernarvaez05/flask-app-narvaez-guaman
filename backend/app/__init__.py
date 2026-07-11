from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)

    from app.models.usuario import Usuario

    with app.app_context():
        db.create_all()

    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({'status': 'ok'}), 200

    @app.route('/api/usuarios', methods=['GET'])
    def listar_usuarios():
        usuarios = Usuario.query.order_by(Usuario.id).all()
        return jsonify([u.to_dict() for u in usuarios]), 200

    @app.route('/api/usuarios/<int:usuario_id>', methods=['GET'])
    def obtener_usuario(usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if usuario is None:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        return jsonify(usuario.to_dict()), 200

    @app.route('/api/usuarios', methods=['POST'])
    def crear_usuario():
        data = request.get_json(silent=True) or {}
        nombre = data.get('nombre', '').strip()
        email = data.get('email', '').strip()
        telefono = data.get('telefono', '').strip()

        if not nombre or not email:
            return jsonify({'error': 'nombre y email son obligatorios'}), 400

        if Usuario.query.filter_by(email=email).first():
            return jsonify({'error': 'Ya existe un usuario con ese email'}), 409

        nuevo = Usuario(nombre=nombre, email=email, telefono=telefono)
        db.session.add(nuevo)
        db.session.commit()
        return jsonify(nuevo.to_dict()), 201

    @app.route('/api/usuarios/<int:usuario_id>', methods=['PUT'])
    def editar_usuario(usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if usuario is None:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        data = request.get_json(silent=True) or {}
        nombre = data.get('nombre', usuario.nombre).strip()
        email = data.get('email', usuario.email).strip()
        telefono = data.get('telefono', usuario.telefono)

        if not nombre or not email:
            return jsonify({'error': 'nombre y email son obligatorios'}), 400

        existente = Usuario.query.filter_by(email=email).first()
        if existente and existente.id != usuario.id:
            return jsonify({'error': 'Ya existe otro usuario con ese email'}), 409

        usuario.nombre = nombre
        usuario.email = email
        usuario.telefono = telefono
        db.session.commit()
        return jsonify(usuario.to_dict()), 200

    @app.route('/api/usuarios/<int:usuario_id>', methods=['DELETE'])
    def eliminar_usuario(usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if usuario is None:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'mensaje': 'Usuario eliminado correctamente'}), 200

    return app
