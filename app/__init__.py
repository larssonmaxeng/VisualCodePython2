from flask import Flask
from app import database
from flask_migrate import Migrate
from app import materiaisPedidos
app = Flask(__name__)
conexao = "sqlite:///fuzzyController.sqlite"
app.config['SECRET_KEY'] = 'q1c2v3b4$$&&'
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACKMODIFICATIONS'] = False
app.config["UPLOAD_FOLDER"] = "/static/arquivos/"
app.register_blueprint(materiaisPedidos.bp_materialPedidos, url_prefix = '/materiaisPedidos')
database.db.init_app(app)
migrate= Migrate(app, database.db)
from app import routes
