from .. import jwt
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def role_required(roles):
    def decorator(function):
        def wrapper(*args, **kwargs):
            #Verificar que el JWT es correcto
            verify_jwt_in_request()
            #obtenemos los claims (peticiones), que estan dentro del JWT
            claims = get_jwt()

            if claims['sub']['role'] in roles:
                return function(*args, **kwargs)
            else:
                return 'Role not allowed', 403 #Erroe 403 no se tiene acceso a este permiso
        return wrapper
    return decorator

@jwt.user_identity_loader
def user_identity_lookup(usuario):
    return {
        'usuarioId': usuario.id,
        'role': usuario.role
    }

@jwt.additional_claims_loader
def add_claims_to_access_tokens(usuario):
    claims= {
        'id': usuario.id,
        'role': usuario.role,
        'email': usuario.email
    }