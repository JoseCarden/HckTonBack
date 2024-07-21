from . import db

class Diagnostico(db.Model):
    __tablename__ = 'diagnostico'
    idDiagno = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('Usuario.idUsuario'))
    idDetalle = db.Column(db.Integer, db.ForeignKey('detalle_diagno.idDetalle'))

    detalle = db.relationship('DetalleDiag', backref='diagnostico', lazy=True)

    def as_dict(self):
        diag_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if self.detalle:
            diag_dict['detalle'] = self.detalle.as_dict()
        return diag_dict