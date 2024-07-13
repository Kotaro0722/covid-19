from flask import Flask

def create_app():
    app=Flask(__name__)
    
    app.config['SECRET_KEY'] = 'dbTeam04'
    
    from .login import login as login_blueprint
    app.register_blueprint(login_blueprint)
        
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .vaccine import vaccine as vaccine_blueprint
    app.register_blueprint(vaccine_blueprint)
    from .condition import condition as condition_blueprint
    app.register_blueprint(condition_blueprint)
    
    return app
