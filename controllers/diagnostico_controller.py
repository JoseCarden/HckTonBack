from flask import Blueprint, request, jsonify
from models import db
from models.diagnostico import Diagnostico

diagnostico_bp = Blueprint('diagnostico_bp', __name__)

@diagnostico_bp.route('/diagnostico', methods=['GET'])
def get_diagnosticos():
    diagnosticos = Diagnostico.query.all()
    return jsonify([diagnostico.as_dict() for diagnostico in diagnosticos])

@diagnostico_bp.route('/diagnostico/<int:id>', methods=['GET'])
def get_diagnostico(id):
    diagnostico = Diagnostico.query.get_or_404(id)
    return jsonify(diagnostico.as_dict())

@diagnostico_bp.route('/diagnostico', methods=['POST'])
def add_diagnostico():
    data = request.json
    nuevo_diagnostico = Diagnostico(
        idUsuario=data['idUsuario'],
        idDetalle=data['idDetalle']
    )
    db.session.add(nuevo_diagnostico)
    db.session.commit()
    return jsonify({'message': 'Diagnóstico añadido correctamente'}), 201
    
@diagnostico_bp.route('/diagnostico/usuario/<int:idUsuario>', methods=['GET'])
def get_diagnosticos_by_usuario(idUsuario):
    diagnosticos = Diagnostico.query.filter_by(idUsuario=idUsuario).all()
    return jsonify([diagnostico.as_dict() for diagnostico in diagnosticos])