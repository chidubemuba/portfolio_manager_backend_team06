from .holding_routes import holding_bp
from .transaction_routes import transaction_bp
from .user_routes import user_bp
from .data_routes import data_bp

def register_routes(app):
    app.register_blueprint(holding_bp, url_prefix='/holding')
    app.register_blueprint(transaction_bp, url_prefix='/transaction')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(data_bp, url_prefix='/data')
    
