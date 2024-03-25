# imports
from flask import Flask
from flask_cors import CORS

from .extensions import db

# Here we're gonna import the blueprints
from producto_entregado.routes import blue
from producto.routes import producto_blue

# Function than create a flask app with CORS
def create_app():
    app = Flask(__name__)
    CORS(app)

    #Database config mysql
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/inventario'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Here we're gonna register the blueprints
    app.register_blueprint(blue)
    app.register_blueprint(producto_blue)
    return app