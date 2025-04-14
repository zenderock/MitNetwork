# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialisation des extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Enregistrement des blueprints
    from app.routes.auth import auth
    from app.routes.users import users
    from app.routes.firewall import firewall
    from app.routes.monitoring import monitoring
    from app.routes.services import services
    from app.routes.logs import logs
    
    app.register_blueprint(auth, url_prefix='/api/auth')
    app.register_blueprint(users, url_prefix='/api/users')
    app.register_blueprint(firewall, url_prefix='/api/firewall')
    app.register_blueprint(monitoring, url_prefix='/api/monitoring')
    app.register_blueprint(services, url_prefix='/api/services')
    app.register_blueprint(logs, url_prefix='/api/logs')
    
    # Création des tables de la base de données (en développement)
    with app.app_context():
        db.create_all()
    
    return app