def create_app(name: str):
    from flask import Flask
    from .config import flask_configs
    from .blueprints import all_blueprints

    app = Flask(name)
    app.config.update(flask_configs)
    [app.register_blueprint(blueprint) for blueprint in all_blueprints]

    return app

__all__ = [
    'create_app',
]