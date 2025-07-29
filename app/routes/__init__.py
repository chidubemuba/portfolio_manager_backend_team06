from .portfolio_routes import portfolio_bp
from .transaction_routes import transaction_bp
from .user_routes import user_bp

def register_routes(app):
    app.register_blueprint(portfolio_bp, url_prefix='/portfolio')
    app.register_blueprint(transaction_bp, url_prefix='/transaction')
    app.register_blueprint(user_bp, url_prefix='/user')
    
