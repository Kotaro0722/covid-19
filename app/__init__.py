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

    # from .action import action as action_blueprint
    # app.register_blueprint(action_blueprint)

    # from .action import action_config as action_config_blueprint
    # app.register_blueprint(action_config_blueprint)

    # from .greet import greet as greet_blueprint
    # app.register_blueprint(greet_blueprint, url_prefix='/greet')

    # from .calculate import calculate as calculate_blueprint
    # app.register_blueprint(calculate_blueprint, url_prefix='/calculate')

    from .related import related as related_blueprint
    app.register_blueprint(related_blueprint)

    from .related import related_table as related_table_blueprint
    app.register_blueprint(related_table_blueprint)    

    from .related import related_search_table as related_search_table_blueprint
    app.register_blueprint(related_search_table_blueprint)

    from .related import admin_action as admin_action_blueprint
    app.register_blueprint(admin_action_blueprint)

    from .close_contact import close_contact as close_contact_blueprint
    app.register_blueprint(close_contact_blueprint)

    from .infected import infected as infected_blueprint
    app.register_blueprint(infected_blueprint)

    from .vaccine import vaccine as vaccine_blueprint
    app.register_blueprint(vaccine_blueprint)

    # from .action import action as action_blueprint
    # app.register_blueprint(action_blueprint)

    # from .action import action_config as action_config_blueprint
    # app.register_blueprint(action_config_blueprint)

    # from .greet import greet as greet_blueprint
    # app.register_blueprint(greet_blueprint, url_prefix='/greet')

    # from .calculate import calculate as calculate_blueprint
    # app.register_blueprint(calculate_blueprint, url_prefix='/calculate')

    
    from .login import login_config as login_config_blueprint
    app.register_blueprint(login_config_blueprint)

    from .action import action as action_blueprint
    app.register_blueprint(action_blueprint)

    from .action import action_config as action_config_blueprint
    app.register_blueprint(action_config_blueprint)
    
    return app
