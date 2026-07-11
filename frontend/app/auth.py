from flask_login import UserMixin


class AdminUser(UserMixin):
    """
    Representa al único administrador de la aplicación.
    No vive en base de datos: se valida contra las variables de
    entorno ADMIN_USERNAME / ADMIN_PASSWORD_HASH definidas en Config.
    """

    def __init__(self, username):
        self.id = username
