from flask import Flask

def create_app():
    app=Flask(__name__)
    
    app.config['SECRET_KEY'] = 'dbTeam04'
    
    from .login import login as login_blueprint
    app.register_blueprint(login_blueprint)
    
    from .login import login_config as login_config_blueprint
    app.register_blueprint(login_config_blueprint)

    from .action import action as action_blueprint
    app.register_blueprint(action_blueprint)

    from .action import action_config as action_config_blueprint
    app.register_blueprint(action_config_blueprint)
        
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .vaccine import vaccine as vaccine_blueprint
    app.register_blueprint(vaccine_blueprint)
    
    return app
