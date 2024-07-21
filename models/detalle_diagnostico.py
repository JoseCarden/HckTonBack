from . import db
from datetime import datetime, timezone,timedelta

class DetalleDiag(db.Model):
    __tablename__ = 'detalle_diagno'
    idDetalle = db.Column(db.Integer, primary_key=True)
    imagen = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precision = db.Column(db.Float, nullable=False)
    tipo_enfermedad = db.Column(db.String(50), nullable=False)
    recomend=db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.Date, default=datetime.now)


    def __init__(self, imagen, descripcion, precision, tipo_enfermedad, recomend,fecha_creacion):
        self.imagen = imagen
        self.descripcion = descripcion
        self.precision = precision
        self.tipo_enfermedad = tipo_enfermedad
        self.recomend = recomend
        self.fecha_creacion = fecha_creacion
        
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
