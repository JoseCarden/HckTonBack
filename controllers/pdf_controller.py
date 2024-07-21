from flask import Blueprint, request, send_file
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
from PIL import Image
import datetime
from dateutil import parser
import locale 

pdf_bp = Blueprint('pdf', __name__)

# Definir la ruta base donde se guardan las imágenes
IMAGE_BASE_PATH = 'static/uploads/'

@pdf_bp.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    data = request.json
    user_data = data.get('user_data', {})
    diagnosis_data = data.get('diagnosis_data', {})
    buffer = BytesIO()

    # Crear un canvas de ReportLab
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    mid_width = width / 2.0

    # Título del reporte
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(mid_width, height - 50, "Reporte de Diagnóstico")

    # Datos del Usuario
    c.setFont("Helvetica-Bold", 20)
    nombre_completo = f"{user_data.get('nombre', '')} {user_data.get('apell', '')}"
    c.drawCentredString(mid_width, height - 85, nombre_completo)


    c.setFont("Helvetica", 10)
    y_position = height - 100

    # Información del usuario
    user_info = [
        ("Edad:", f"{user_data.get('edad', '')} años"),
        ("Teléfono:", user_data.get("telefono", "")),
        ("DNI:", user_data.get("dni", "")),
        ("Dirección:", user_data.get("direccion", "")),
        ("Peso:", f"{user_data.get('peso', '')} kg"),
        ("Altura:", f"{user_data.get('altura', '')} cm"),
    ]
    
    for label, value in user_info:
        text = f"{label} {value}"
        c.drawString(50, y_position, text)
        y_position -= 15

    # Línea divisoria
    c.line(40, y_position, width - 40, y_position)
    y_position -= 20

    # Datos del Diagnóstico
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, y_position, "Diagnóstico Presuntivo")
    y_position -= 25

    c.setFont("Helvetica", 10)
    precision = diagnosis_data.get('precision', 0.0)
    percentage_precision = precision * 100
    formatted_precision = f"{percentage_precision:.0f}%"
    
    # Etiquetas y valores de los datos del diagnóstico
    diagnosis_info = {
        "Tipo de enfermedad": diagnosis_data.get("tipo_enfermedad", ""),
        "Descripción": diagnosis_data.get("descripcion", ""),
        "Precisión": formatted_precision,
        "Recomendación": diagnosis_data.get("recomend", ""),
    }

    for label, value in diagnosis_info.items():
        text = f"{label}: {value}"
        c.drawString(50, y_position, text)
        y_position -= 15

    # Imagen del diagnóstico (si existe)
    image_path = diagnosis_data.get("imagen", "")
    if image_path:
        full_image_path = os.path.join(IMAGE_BASE_PATH, image_path)
        if os.path.exists(full_image_path):
            img = Image.open(full_image_path)
            img_width, img_height = img.size
            img_aspect_ratio = img_width / img_height
            display_width = 200
            display_height = display_width / img_aspect_ratio
            x_position = (width - display_width) / 2.0
            c.drawImage(ImageReader(img), x_position, y_position - display_height, width=display_width, height=display_height)
            y_position -= display_height + 15
        else:
            c.drawString(50, y_position, "Error al cargar la imagen")
            y_position -= 15
      # Firma y fecha
    fecha_creacion = diagnosis_data.get("fecha_creacion")
    print(f"Fecha de creación recibida: {fecha_creacion}")  # Depuración: imprimir la fecha recibida
     # Configurar la localización a español
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    
    if fecha_creacion:
        try:
            # Convertir la fecha a un formato legible
            if isinstance(fecha_creacion, str):
                fecha = parser.parse(fecha_creacion).strftime('%d de %B del %Y')
            else:
                fecha = fecha_creacion.strftime('%d de %B del %Y')
        except ValueError:
            fecha = "Fecha no válida"
    else:
        fecha = "Fecha no proporcionada"

    y_position -= 35 
    c.setFont("Helvetica", 10)
    c.drawString(50, y_position, "Se expide el presente a solicitud del interesado.")
    y_position -= 80
    c.drawRightString(width - 50, y_position, f"Fecha: {fecha}")
    c.showPage()
    c.save()

    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name='reporte_diagnostico.pdf', mimetype='application/pdf')