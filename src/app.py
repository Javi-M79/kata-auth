from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

from infrastructure.db.database import db
from infrastructure.db.models.auth import Auth
from infrastructure.db.models.user import User


def create_app():
    app = Flask(__name__)

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

        return jsonify({"message": "Contraseña verificada correctamente."}), 401

    # REGISTER
    @app.route("/register", methods=['POST'])
    def register():

            data = request.get_json()
            if not data:
                return jsonify({"error:" "El cuerpo de la solicitud debe ser un JSON Valido"}), 400

            username = data.get("username")
            password = data.get("password")

            # Si no introduce los datos
            if not username or not password:
                return jsonify({"error": "Faltan campos obligatorios."}), 400

            # Verificacion de que el usuario existe:
            if User.select().where(User.username == username).exists():
                return jsonify({"error": "El nombre de usuario ya esta registrado"}), 409

            # Cifrado de contrasenya
            hashed_password = generate_password_hash(password)

            # Registrar nuevo usuario
            user = User.create(username=username, password=hashed_password)
            return jsonify({"message": f"Usuarion {user.username} registrado correctamente"}), 201


    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
