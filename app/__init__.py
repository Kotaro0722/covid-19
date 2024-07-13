from flask import Flask

def create_app():
    app=Flask(__name__)
    
    from .login import login as login_blueprint
    app.register_blueprint(login_blueprint)
        
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .vaccine import vaccine as vaccine_blueprint
    app.register_blueprint(vaccine_blueprint)
    
    return app
