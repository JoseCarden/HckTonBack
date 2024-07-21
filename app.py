from flask import Flask
from config import Config
from models import db
from controllers.usuario_controller import usuario_bp
from controllers.detalle_diagnostico_controller import detalle_diag_bp
from controllers.diagnostico_controller import diagnostico_bp
from controllers.pdf_controller import pdf_bp
#from controllers.auth import auth_bp
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

app = Flask(__name__)
CORS(app)
jwt = JWTManager(app)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(usuario_bp)
app.register_blueprint(detalle_diag_bp)
app.register_blueprint(diagnostico_bp)
app.register_blueprint(pdf_bp)
#app.register_blueprint(auth_bp)

@app.before_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)