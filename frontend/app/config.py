import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-temporal-cambiar-en-produccion')

    # URL interna del backend, resuelta por el DNS interno de Docker
    # (nombre del servicio 'backend' en la red 'web'). Nunca se expone
    # al navegador del usuario: todas las llamadas son server-side.
    BACKEND_URL = os.environ.get('BACKEND_URL', 'http://backend:5000')

    # Credenciales del único administrador de la aplicación.
    # ADMIN_PASSWORD_HASH se genera con werkzeug.security.generate_password_hash
    # y se guarda ya hasheada en el .env — nunca la contraseña en texto plano.
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD_HASH = os.environ.get('ADMIN_PASSWORD_HASH', '')
