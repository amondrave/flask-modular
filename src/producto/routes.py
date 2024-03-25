from flask import Blueprint, jsonify, request, abort
from app.extensions import db
from .models import Producto

producto_blue=Blueprint('producto',__name__,url_prefix='/producto')

@producto_blue.route('/', methods=['POST'])
def new_product():
    data = request.json
    try:
        producto = Producto(nombre=data['nombre'], tipo=data['tipo'], disponible=1)
        db.session.add(producto)
        db.session.commit()
        return jsonify({"message": "Producto agregado correctamente"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "El producto no pudo ser agregado. Verifica los datos y vuelve a intentarlo."}), 400


@producto_blue.route('/productos', methods=['GET'])
def get_all():
    productos = Producto.query.all()
    return jsonify([producto.serialize() for producto in productos])