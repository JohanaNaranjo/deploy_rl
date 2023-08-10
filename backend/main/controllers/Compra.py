#Recibe los datos externos y envia los datos, devuelve los datos a la vista. Interactua con el exterior de la aplicación es decir con el cliente

from flask_restful import Resource
from main.maps import CompraSchema
from main.services import CompraService
from flask import request

compra_schema = CompraSchema()
compra_service = CompraService()

class CompraController(Resource):

    def get(self, id):
        compra = compra_service.obtener_compra_con_descuento(id)
        return  compra_schema.dump(compra, many=False) #dump se utiliza para enviar un dato
    

class ComprasController(Resource):

    def post(self):
        compra = compra_schema.load(request.get_json()) #load se utiliza para reibir un dato
        return compra_schema.dump(compra_service.agregar_compra(compra), many = False)
    
    
    


