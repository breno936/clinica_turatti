from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail, Message

# Inicializando as extensões
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'views.login'  # <-- aqui está o segredo
migrate = Migrate()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '6fa8c97d5a09c8f44b578b6262e0a167'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinica.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configuração do servidor de e-mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Usando Gmail como exemplo
    app.config['MAIL_PORT'] = 587  # Porta para TLS
    app.config['MAIL_USE_TLS'] = True  # Usar TLS
    app.config['MAIL_USE_SSL'] = False  # Não usar SSL
    app.config['MAIL_USERNAME'] = 'seu_email@gmail.com'  # E-mail do remetente
    app.config['MAIL_PASSWORD'] = 'sua_senha_de_email'  # Senha do remetente (ou senha de app do Gmail)
    app.config['MAIL_DEFAULT_SENDER'] = 'seu_email@gmail.com'  # E-mail de remetente

    # Inicializando as extensões
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)  # Inicializando Flask-Mail
    migrate.init_app(app, db)

    # Função para carregar o usuário
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  # Importando User aqui, após o db ser inicializado
        return User.query.get(int(user_id))

    # Importando os modelos e registrando os blueprints depois de inicializar o db
    from app import views
    app.register_blueprint(views.views_bp)

    return app
