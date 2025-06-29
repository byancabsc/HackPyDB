from flask import Flask
from app.routes.auth import auth_bp
from app.routes.goals_mssql import goals_bp
from app.routes.home import home_bp
from app.routes.todo_postgress import todo_bp
from app.routes.mission_mysql import mission_bp
from app.routes.vulnpanel import vuln_bp

def create_app():
    app = Flask(
        __name__,
        template_folder="templates",  # relativo ao diretório atual (__name__)
        static_folder="static"
    )

    app.secret_key = 'chave_supersecreta'

    app.register_blueprint(auth_bp)
    app.register_blueprint(goals_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(todo_bp)
    app.register_blueprint(mission_bp)
    app.register_blueprint(vuln_bp)

    
    return app
