from flask import Flask

def create_app():
    app=Flask(__name__)
    
    from .login import login as login_blueprint
    app.register_blueprint(login_blueprint)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .action import action as action_blueprint
    app.register_blueprint(action_blueprint)

    from .action import action_config as action_config_blueprint
    app.register_blueprint(action_config_blueprint)

    # from .greet import greet as greet_blueprint
    # app.register_blueprint(greet_blueprint, url_prefix='/greet')

    # from .calculate import calculate as calculate_blueprint
    # app.register_blueprint(calculate_blueprint, url_prefix='/calculate')

    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .action import action as action_blueprint
    app.register_blueprint(action_blueprint)

    from .action import action_config as action_config_blueprint
    app.register_blueprint(action_config_blueprint)

    # from .greet import greet as greet_blueprint
    # app.register_blueprint(greet_blueprint, url_prefix='/greet')

    # from .calculate import calculate as calculate_blueprint
    # app.register_blueprint(calculate_blueprint, url_prefix='/calculate')

    return app
