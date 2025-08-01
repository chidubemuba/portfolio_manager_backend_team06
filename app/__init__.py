from flask import Flask
from flask_cors import CORS

from .models import db
from .config import DevelopmentConfig
from .routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    CORS(app)  
    
    db.init_app(app)
    register_routes(app)
    
    with app.app_context():
        db.create_all()

    return app

