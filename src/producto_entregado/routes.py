# imports
from flask import Blueprint, jsonify, request, abort
from flask_pymongo import ObjectId, MongoClient
from datetime import datetime, timedelta # for the user registration time


user = 'root'
password = 'secret'
connection_str = f'mongodb://{user}:{password}@localhost:27017/'
client = MongoClient(connection_str)
db = client.inventario.producto_entregado

# BLUEPRINT CONFIGS
#           blueprint name                       path
#                  ⇩                              ⇩
blue = Blueprint('producto_entregado', __name__, url_prefix='/producto-entregado')

# Create a new user
@blue.route('/', methods=['POST'])
def new_product_mongo():

    # Catching the values
    user = request.json['user']
    producto = request.json['producto']
    serial = request.json['serial']
    tipo = request.json['tipo']
    date = request.json['date']
    disponible = False

    
    # User registration
    id = db.insert_one({
        'user' : user,
        'producto' : producto,
        'date' : date,
        'tipo' : tipo,
        'serial': serial,
        'disponible': disponible
    })

    return jsonify({'_id' : str(ObjectId(id.inserted_id))})

@blue.route('/todos', methods=['GET'])
def get_all():
    docs = []
    for doc in db.find():
        docs.append({
            'producto' : doc['producto'],
            'serial' : doc['serial'],
            'date' : doc['date'],
            '_id' : str(ObjectId(doc['_id'])),
            'tipo': doc['tipo'],
            'disponible': doc['disponible']
        })
    return jsonify(docs)

@blue.route('/entregar/<serial>', methods=['PUT'])
def set_disponible(serial):
    db.update_one(
        {'serial': serial},
        {'$set': {'disponible':True}}
    )
    return jsonify({"message": "Producto entregado marcado correctamente"},200)