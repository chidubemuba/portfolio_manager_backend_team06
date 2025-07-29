from .portfolio_routes import portfolio_bp

def register_routes(app):
    app.register_blueprint(portfolio_bp, url_prefix='/api/portfolio')
    
