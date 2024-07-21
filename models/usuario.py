from . import db,bcrypt
from datetime import datetime
class Usuario(db.Model):
    __tablename__ = 'Usuario'
    idUsuario = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.String(20), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    apell = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    direccion = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    sexo = db.Column(db.String(10))
    fecha_nac = db.Column(db.Date)
    peso = db.Column(db.Float)
    altura = db.Column(db.Float)
    rol = db.Column(db.String(50), nullable=False)

    #def set_password(self, password):
     #   self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    #def check_password(self, password):
     #   return bcrypt.check_password_hash(self.password, password)

    def as_dict(self):
        result = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if self.fecha_nac:
            result['fecha_nac'] = self.fecha_nac.strftime('%d %b %Y')  # Formatear fecha
        return result

