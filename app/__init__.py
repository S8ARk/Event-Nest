import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt()

def create_app(config_class='app.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Register Blueprints
    from app.routes import main, auth, user, events, registrations
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(events.bp)
    app.register_blueprint(registrations.bp)

    return app
