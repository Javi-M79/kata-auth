from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash, check_password_hash

from core.services.auth_service import AuthService
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
        sign = data.get('sign')
        # Validacion de datos necesarios
        if not mail or not password or not sign:
            return jsonify({"error": "Faltan credenciales."}), 400

        try:
            # Validacion de la firma
            AuthService.validate_sign(mail, password, sign)

            # Busqueda del usuario en la base de datos.
            user = UserModel.get(UserModel.mail == mail)
            # Verificacion de contrasenya
            if not check_password_hash(user.password, password):
                return jsonify({"error": "Usuario o contraseña incorrectos."}), 401

            tokens = AuthService.generate_tokens(user.id)
            return jsonify({
                "user": {
                "username": user.username,
                "person_id": user.id,
                    "activated": True
             },
                "token": tokens["access_token"],
                "refreshToken": tokens["refresh_token"]
            }), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 401

        except UserModel.DoesNotExist:
            return jsonify({"error": "Usuario o contraseña incorrectos."}), 401

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
