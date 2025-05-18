import jwt
from datetime import datetime, timedelta
from config import Config

def generar_token(payload, exp_seconds=10):
    payload['exp'] = datetime.utcnow() + timedelta(seconds=exp_seconds)
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
    return token

def verificar_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
