from alembic.util import status
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config.config import Config

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

def create_first_user():
    from flaskr.models.usuarios import Usuarios, Status
    data = Usuarios.query.filter_by(status=Status.ADM).count()
    if data == 0:
        new_user = Usuarios(name='Admin', uid='admin', email='admin@admin.com', status=Status.ADM)
        new_user.set_password('admin')
        db.session.add(new_user)
        db.session.commit()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    with app.app_context():
        from .routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

    return app