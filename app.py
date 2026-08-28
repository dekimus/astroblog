from flask import Flask
from datetime import datetime
from extensions import db, login_manager
from config import Config
from  models import User
import click



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    ## Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    
    @app.cli.command("create-admin")
    @click.argument("username")
    @click.password_option()
    def create_admin(username, password):
        """Crea un usuario administrador."""
        if User.query.filter_by(username=username).first():
            click.echo(f"El usuario '{username}' ya existe.")
            return
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f"Usuario '{username}' creado correctamente.")

    with app.app_context():
        db.create_all()

    from routes.auth import auth_bp
    from routes.blog import blog_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)
    
    @app.context_processor
    def inject_now():
        return {"now": datetime.utcnow()}

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)