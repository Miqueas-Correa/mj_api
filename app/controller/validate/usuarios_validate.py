import re
from flask import jsonify
from email_validator import validate_email, EmailNotValidError

def validate_usuario_input(data):
    errors = []

    nombre = data.get("nombre")
    email = data.get("email")
    telefono = data.get("telefono")
    contrasenia = data.get("contrasenia")

    if not all([nombre, email, telefono, contrasenia]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    if not isinstance(nombre, str) or len(nombre.strip()) < 2:
        errors.append("El nombre debe tener al menos 2 caracteres.")

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(pattern, email or ""):
        errors.append("El email no es válido.")

    try:
        validate_email(email)
    except EmailNotValidError:
        errors.append("El email no es válido.")

    if len(contrasenia or "") < 6:
        errors.append("La contraseña debe tener al menos 6 caracteres.")

    return (jsonify({"errors": errors}), 400) if errors else None