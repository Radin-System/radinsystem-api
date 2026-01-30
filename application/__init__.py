def create_app(name: str):
    from flask import Flask
    from application.config import app_config
    from .blueprints import all_blueprints

    app = Flask(name)
    app.config['SECRET_KEY'] = app_config.flask_secret_key
    [app.register_blueprint(blueprint) for blueprint in all_blueprints]

    return app


__all__ = [
    'create_app',
]