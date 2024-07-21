from flask import Blueprint, request,jsonify
from models import db
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity,create_access_token
from models.usuario import Usuario
from werkzeug.security import check_password_hash,generate_password_hash
usuario_bp=Blueprint('usuario_bp', __name__)

@usuario_bp.route('/usuario', methods=['GET'])
def get_usuarios():
    usuarios=Usuario.query.all()
    return jsonify([usuario.as_dict() for usuario in usuarios])
@usuario_bp.route('/usuario/<int:id>', methods=['GET'])
def get_usuario(id):
    usuario=Usuario.query.get_or_404(id)
    return jsonify(usuario.as_dict())


@usuario_bp.route('/usuario', methods=['POST'])
def add_usuario():
    data = request.json
    hashed_password = generate_password_hash(data['password'])
    nuevo_usuario = Usuario(
        dni = data['dni'],
        nombre = data['nombre'],
        apell = data['apell'],
        telefono = data['telefono'],
        edad = data['edad'],
        direccion = data['direccion'],
        usuario = data['usuario'],
        email = data['email'],
        password = hashed_password,  # Contraseña hasheada
        sexo = data.get('sexo'),
        fecha_nac = data.get('fecha_nac'),
        peso = data.get('peso'),
        altura = data.get('altura'),
        rol = data['rol']
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({'message': 'Usuario añadido correctamente'}), 201

@usuario_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    usuario = data.get('usuario')
    password = data.get('password')
    
    # Buscar usuario por nombre de usuario
    user = Usuario.query.filter_by(usuario=usuario).first()
    
    if user and check_password_hash(user.password, password):
        # Generar token JWT
        access_token = create_access_token(identity=user.idUsuario)
        
        # Preparar los datos del usuario para devolver (sin la contraseña)
        user_data = user.as_dict()
        del user_data['password']
        
        # Devolver respuesta con el token JWT y los datos del usuario
        return jsonify({
            'message': 'Inicio de sesión exitoso',
            'usuario': user_data,
            'access_token': access_token
        }), 200
    else:
        return jsonify({'message': 'Nombre de usuario o contraseña incorrectos'}), 401

@usuario_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    usuario = Usuario.query.get_or_404(current_user_id)
    user_data = usuario.as_dict()
    del user_data['password']  # No incluir la contraseña en la respuesta
    return jsonify(user_data)