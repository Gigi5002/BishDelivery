# fastapi-core/src/infrastructure/security/password.py
import bcrypt

def hash_password(password: str) -> str:
    """Превращает обычный пароль в защищенный хэш"""
    # Генерируем соль (случайные символы) и солим пароль
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')