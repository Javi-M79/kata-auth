from datetime import datetime
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash

from core.services.auth_service import AuthService
from domain.ports.inbound_dto.login_dto import LoginDTO
from domain.ports.inbound_dto.register_dto import RegisterDTO
from infrastructure.db.database import db
from infrastructure.db.models.auth_model import AuthModel
from infrastructure.db.models.user_model import UserModel


def create_app():

    load_dotenv()
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

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

    # /PING. ENDPOINT DE PARA PROBAR CONEXION
    @app.route('/ping', methods=['GET'])
    def ping():
        # Endpoint para probar la conexion al servidor
        return jsonify({"message": "Servidor conectado correctamente"}), 200

    # /LOGIN ENDPOINT PARA EL LOGIN DE USUARIO
    @app.route('/login', methods=['POST'])
    def login():
        try:

            data = request.get_json()
            if not data:
                return jsonify({"error": "El cuerpo de la solicitud debe ser un JSON valido."}), 400

            # Crear instancia de loginDTO
            login_data = LoginDTO(
                mail=data.get("mail"),
                password=data.get("password"),
                sign=data.get("sign")
            )

            # Validacion de la firma con los datos recuperados en login_data. Validamos la firma antes para no exponer
            # errores especificos como contrasenya incorrecta. Por eso la verificamos después.
            AuthService.validate_sign(login_data.mail, login_data.password, login_data.sign, )

            # Busqueda del usuario en la base de datos (Compara el 'UserModel' de la BD con el usuario logueado 'login_data')
            user = UserModel.get(UserModel.mail == login_data.mail)
            # Verificacion de contrasenya
            if not check_password_hash(user.password, login_data.password):
                return jsonify({"error": "Usuario o contraseña incorrectos."}), 401
            # Generar tokens
            tokens = AuthService.generate_tokens(user.id)
            #Guardar los tokens en la base de datos.
            AuthService.store_refresh_token(user.id, tokens["refresh_token"])

            return jsonify({
                "user": {
                    "username": user.username,
                    "person_id": user.id,
                    "activated": True
                },
                "access_token": tokens["access_token"],
                "refresh_token": tokens["refresh_token"]
            }), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 401

        except UserModel.DoesNotExist:
            return jsonify({"error": "Usuario o contraseña incorrectos."}), 401

    # /REGISTER ENDPOINT PARA REGISTRO DE USUARIO
    @app.route("/register", methods=['POST'])
    def register():

        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "El cuerpo de la solicitud debe ser un JSON válido."}), 400

            # Creacion de una instancia de RegisterDTO. Recoge los datos introducidos por el usuario.
            register_data = RegisterDTO(username=data.get("username"),
                                        mail=data.get("mail"),
                                        password=data.get("password"))
            # Comprobacion de que el usuario no existe en la base de datos.
            if UserModel.select().where(UserModel.mail == register_data.mail).exists():
                return jsonify({"error": "El usuario ya está registrado."}), 409

            # Si le usuario no existe procedemos al cifrado de contrasenya.
            hashed_password = generate_password_hash(register_data.password)

            # Creamos el usuario en la base de datos (UserModel) a partir del register_data.
            user = UserModel.create(username=register_data.username,
                                    mail=register_data.mail,
                                    password=hashed_password)
            return jsonify({"message": f"Usuario {user.username} registrado correctamente."}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    # /AUTH ENDPOINT DE AUTENTICACION.
    @app.route("/auth", methods=['POST'])
    @jwt_required()
    def auth():
        try:
            user_id = get_jwt_identity()
            return jsonify({"message": f"Token valido, user_id = {user_id}"}), 200
        except Exception as e:
            return jsonify({"error": "Token invalido"}), 400

    # / REFRESH ENDPOITN DE GENERACION DE NUEVO TOKEN DE REFRESCO
    @app.route('/refresh', methods=['POST'])
    @jwt_required(refresh=True)
    def refresh():

        try:
            #Obtenemnos el id del usuario desde el token
            user_id = get_jwt_identity()

            #Buscamos el token en la base de datos

            token = AuthModel.get(AuthModel.user_id == user_id)
            print(f"Token encontrado en la base de datos: {token.refresh_token}")

            #Validamos que no haya caducado
            if token.expired_date <datetime.utcnow():
                return jsonify({"error": "El token ha caducado."}), 401

            #Generar nuevos tokens
            new_tokens = AuthService.generate_tokens(user_id)
            print(f"Nuevos tokens generados: {new_tokens}")

            #Actualizacion de fecha de uso.
            token.update_date = datetime.utcnow()
            token.save()

            return jsonify(new_tokens), 200
        except AuthModel.DoesNotExist:
            return jsonify({"error": "El token no existe."}), 401

    # /USER. ENDOPOINT QUE MUESTRA LA LISTA DE USUARIOS REGISTRADOS
    @app.route('/users', methods=['GET'])
    def list_user():
        users = UserModel.select()  # RFEcupera todos los usuarios
        users_list = []  # Lista donde guardaremos todos los usuarios
        # Recorremos los usuarios de la base de datos

        for user in users:
            # Anyadimos los usuarios a la lista
            users_list.append({
                "id": str(user.id),  # Casteamos al ser un UUID
                "Username": (user.username),
                "Mail": (user.mail)

            })

            # Devolvemos la lista en formato JSON
        return jsonify({"Users": users_list}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
