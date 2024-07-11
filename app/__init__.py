from flask import Flask

def create_app():
    app=Flask(__name__)
    
    from .login import login as login_blueprint
    app.register_blueprint(login_blueprint)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
