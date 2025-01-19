from datetime import timedelta

from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
from infrastructure.db.database import db
from infrastructure.db.models.auth import Auth
from infrastructure.db.models.user import User


def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "1234"


    with app.app_context():
        db.connect()
        db.create_tables([Auth, User], safe=True)
        db.close()

    # Conexion a la base de datos antes de cada solicitud
    @app.before_request
    def before_request():
        if db.is_closed():
            db.connect()

    # PING
    @app.route('/ping', methods=['GET'])
    def ping():
        # Endpoint para probar la conexion al servidor
        return jsonify({"message": "Servidor conectado correctamente"}), 200

    # LOGIN
    @app.route('/login', methods=['POST'])
    def login():

        data = request.get_json()

        if not data:
            return jsonify({"error": "El cuerpo de la solicitud debe ser un JSON valido."})

        username = data.get('username')
        password = data.get('password')

        # Verificacion de datos
        if not username or not password:
            return jsonify({"error": "Faltan credenciales."}), 400

        # Busqueda del usuario en la base de datos.
        try:
            user = User.get(User.username == username)
        except User.DoesNotExist:
            return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

        # Verificacion de contrasenya
        if not check_password_hash(user.password, password):
            return jsonify({"error": "Usuario o contraseña incorrectos."}), 401

    # Generacion de Tomen JWT y refresh Token
        acces_token = create_access_token(identity=user.id, expires_delta=timedelta(days=2))
        refresh_token = create_refresh_token(identity=user.id, expires_delta=timedelta(weeks=1))

    # Devolver los tokens con datos de usuario
        return jsonify({
            "user": {
                "username": user.username,
                "person_id": user.id,
             "activated": True
             },
            "token": acces_token,
            "refreshToken": refresh_token

            })


    # REGISTER
    @app.route("/register", methods=['POST'])
    def register():
        data = request.get_json()
        if not data:
            return jsonify({"error": "El cuerpo de la solicitud debe ser un JSON válido."}), 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Faltan campos obligatorios."}), 400

        if User.select().where(User.username == username).exists():
            return jsonify({"error": "El nombre de usuario ya está registrado"}), 409

        hashed_password = generate_password_hash(password)

        user = User.create(username=username, password=hashed_password)
        return jsonify({"message": f"Usuario {user.username} registrado correctamente"}), 201

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
