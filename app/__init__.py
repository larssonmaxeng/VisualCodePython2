from flask import Flask
from app import database
from flask_migrate import Migrate
from app import materiaisPedidos
from os.path import abspath, dirname, join
app = Flask(__name__)
conexao =  "sqlite:///fuzzyController.sqlite"
BASE_DIR = dirname(dirname(abspath(__file__)))
SHAPE_DIR = join(BASE_DIR,"app","static","arquivos")
app.config['SECRET_KEY'] = 'q1c2v3b4$$&&'
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACKMODIFICATIONS'] = False
app.config["UPLOAD_FOLDER"] = SHAPE_DIR
app.register_blueprint(materiaisPedidos.bp_materialPedidos, url_prefix = '/materiaisPedidos')
database.db.init_app(app)
#migrate= Migrate(app, database.db)
from app import routes
