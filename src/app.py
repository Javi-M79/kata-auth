from datetime import timedelta

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash

from infrastructure.db.database import db
from infrastructure.db.models.auth_model import AuthModel
from infrastructure.db.models.user_model import UserModel


def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "1234"

    jwt = JWTManager(app)

    with app.app_context():
        db.connect()
        db.create_tables([AuthModel, UserModel], safe=True)
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
            return jsonify({"error": "El cuerpo de la solicitud debe ser un JSON valido."}),400

        mail = data.get('mail')
        password = data.get('password')

        # Verificacion de datos
        if not mail or not password:
            return jsonify({"error": "Faltan credenciales."}), 400

        # Busqueda del usuario en la base de datos.
        try:
            user = UserModel.get(UserModel.mail == mail)
        except UserModel.DoesNotExist:
            return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

        # Verificacion de contrasenya
        if not check_password_hash(user.password, password):
            return jsonify({"error": "Usuario o contraseña incorrectos."}), 401

    # Generacion de Token JWT y refresh Token
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=2))
        refresh_token = create_refresh_token(identity=user.id, expires_delta=timedelta(weeks=1))

    # Devolver los tokens con datos de usuario
        return jsonify({
            "user": {
                "username": user.username,
                "person_id": user.id,
             "activated": True
             },
            "token": access_token,
            "refreshToken": refresh_token

            }),200


    # REGISTER
    @app.route("/register", methods=['POST'])
    def register():
        data = request.get_json()
        if not data:
            return jsonify({"error": "El cuerpo de la solicitud debe ser un JSON válido."}), 400

        username = data.get("username")
        mail = data.get("mail")
        password = data.get("password")

        if not mail or not password:
            return jsonify({"error": "Faltan campos obligatorios."}), 400
        if UserModel.select().where(UserModel.mail == mail).exists():
            return jsonify({"error": "El usuario ya está registrado"}), 409

        hashed_password = generate_password_hash(password)
        user = UserModel.create(username=username, mail=mail, password=hashed_password)
        return jsonify({"message": f"Usuario {user.username} registrado correctamente"}), 201

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
