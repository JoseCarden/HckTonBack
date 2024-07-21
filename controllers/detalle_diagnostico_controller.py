from flask import Blueprint, request, jsonify, send_from_directory
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
import os
import io
from models import db
from models.detalle_diagnostico import DetalleDiag
from datetime import datetime, timezone,timedelta
from flask import Blueprint, request,jsonify
from models import db
from models.detalle_diagnostico import DetalleDiag

detalle_diag_bp=Blueprint('detalle_diag_bp',__name__)
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@detalle_diag_bp.route('/detalle_diag',methods=['GET'])
def get_detalle_diag():
    detalles= DetalleDiag.query.all()
    return jsonify([detalle.as_dict()for detalle in detalles])

@detalle_diag_bp.route('/detalle_diag/<int:id>',methods=['GET'])
def get_detalle_diag_by_id(id):
    detalle=DetalleDiag.query.get_or_404(id)
    return jsonify(detalle.as_dict())

# Cargar el modelo .h5
model = load_model('models/mobile.h5')

# Definir clases de animales
classes = ['PERRO', 'CABALLO', 'ELEFANTE', 'MARIPOSA', 'GALLINA', 'GATO', 'VACA',
               'OVEJA', 'ARAÑA', 'ARDILLA']

@detalle_diag_bp.route('/nuevo_det_diag', methods=['POST'])
def nuevo_detalle_diag():
    if 'imagen' not in request.files:
        return jsonify({'error': 'No se ha subido ninguna imagen'}), 400
    
    file = request.files['imagen']
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    img = Image.open(filepath)
    img = img.resize((224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    
    preds = model.predict(x)
    class_idx = np.argmax(preds[0])
    class_label = classes[class_idx]
    confidence = preds[0][class_idx]
    
    data = request.form
    
    nuevo_detalle = DetalleDiag(
        imagen=filename,  # Guardar solo el nombre del archivo
        descripcion=data['descripcion'],
        precision=float(confidence),
        tipo_enfermedad=class_label,
        recomend=data['recomend'],
        fecha_creacion=datetime.now().date()
    )
    

    return jsonify({
        'message': 'Detalle de diagnóstico añadido correctamente',
        'detalle_diag': {
            'idDetalle': nuevo_detalle.idDetalle,
            'imagen': filename,
            'descripcion': data['descripcion'],
            'precision': float(confidence),
            'tipo_enfermedad': class_label,
            'recomend': data['recomend'],
            'fecha_creacion': nuevo_detalle.fecha_creacion.strftime('%Y-%m-%d'),
            'path': filepath
        }
    }), 201

@detalle_diag_bp.route('/guardar_det_diag', methods=['POST'])
def guardar_detalle_diag():
    if 'imagen' not in request.files:
        return jsonify({'error': 'No se ha subido ninguna imagen'}), 400
    
    file = request.files['imagen']
    if file.filename == '':
        return jsonify({'error': 'Nombre de archivo no válido'}), 400
    
    # Asegurarse de que el nombre del archivo sea seguro
    original_filename = secure_filename(file.filename)
    filename, _ = os.path.splitext(original_filename)
    filename = f"{filename}.jpeg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    img = Image.open(filepath)
    img = img.resize((224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    
    preds = model.predict(x)
    class_idx = np.argmax(preds[0])
    class_label = classes[class_idx]
    confidence = preds[0][class_idx]
    
    data = request.form
    
    nuevo_detalle = DetalleDiag(
        imagen=filename,  # Guardar solo el nombre del archivo
        descripcion=data['descripcion'],
        precision=float(confidence),
        tipo_enfermedad=class_label,
        recomend=data['recomend'],
        fecha_creacion=datetime.now().date()
    )
    
    db.session.add(nuevo_detalle)
    db.session.commit()
    
    return jsonify({
        'message': 'Detalle de diagnóstico añadido correctamente',
        'detalle_diag': {
            'idDetalle': nuevo_detalle.idDetalle,
            'imagen': filename,
            'descripcion': data['descripcion'],
            'precision': float(confidence),
            'tipo_enfermedad': class_label,
            'recomend': data['recomend'],
            'fecha_creacion': nuevo_detalle.fecha_creacion.strftime('%Y-%m-%d')
        }
    }), 201

@detalle_diag_bp.route('/uploads/<filename>', methods=['GET'])
def get_image(filename):
    return send_from_directory(UPLOAD_FOLDER,filename)

# # Cargar el modelo .h5
# model = load_model('models/osteoporosis_classifier.h5')
# def preprocess_image(image_path):
#     img = Image.open(image_path).convert('RGB')  # Asegurarse de que la imagen tiene tres canales (RGB)
#     img = img.resize((224, 224))
#     img = np.array(img) / 255.0
#     img = np.expand_dims(img, axis=0)
#     return img
# @detalle_diag_bp.route('/detalle_diag', methods=['POST'])
# def add_detalle_diag():
#     if 'file' not in request.files:
#         return jsonify(error='No file provided'), 400

#     file = request.files['file']
#     image_path = f'./temp/{file.filename}'
#     file.save(image_path)

#     image = preprocess_image(image_path)
#     prediction = model.predict(image)
#     os.remove(image_path)

#     prediction_class = int(np.argmax(prediction))
#     class_names = ["Normal", "Osteoporosis"]
#     confidence = float(np.max(prediction)) * 100

#     data = request.form 
#     # Diagnóstico presuntivo basado en la predicción
#     if prediction_class == 1:
#         diagnosis = "Diagnóstico presuntivo: Posible enfermedad esquelética osteoporosis"
#     else:
#         diagnosis = "Diagnóstico presuntivo: Usted no tiene osteoporosis"

#     nuevo_detalle = DetalleDiag(
#         descripcion=diagnosis,
#         tipo_enfermedad=class_names[prediction_class],
#         precision=f'{confidence:.2f}',
#         imagen=file.filename,
#         recomend=data['recomend']
#     )

#     # Agregar la instancia a la sesión de la base de datos
#     db.session.add(nuevo_detalle)
#     db.session.commit()  # Confirmar la transacción para guardar los cambios
    
#     response = {
#         'descripcion': diagnosis,
#         'tipo_enfermedad': class_names[prediction_class],
#         'precision': f'{confidence:.2f}',
#         'imagen': file.filename,
#         'recomend': data['recomend']
#     }
#     return jsonify(response)