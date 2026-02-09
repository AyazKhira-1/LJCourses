from flask import Flask
from app.config import Config
from app.utils import get_current_user_from_session
import os

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(config_class)

    # Context processors
    @app.context_processor
    def inject_user():
        return dict(current_user=get_current_user_from_session())

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register Blueprints
    from app.routes import auth, student, course
    app.register_blueprint(auth.bp)
    app.register_blueprint(student.bp)
    app.register_blueprint(course.bp)

    return app
