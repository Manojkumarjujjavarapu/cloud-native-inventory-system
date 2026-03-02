from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()

        if claims.get("role") != "admin":
            return {"message": "Admins only"}, 403

        return fn(*args, **kwargs)

    return wrapper