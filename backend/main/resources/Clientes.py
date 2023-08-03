from flask_restful import Resource
#Esta libreria sirve para devolver las consultas o los recursos que le llguen peticiones de clientes al servidor 
from flask import jsonify, request
from .. import db
from main.models import UsuarioModel
from main.auth.decorators import role_required
from flask_jwt_extended import get_jwt_identity

#Se define esta clase para obtener los recursos de la appi, borrar, colocar, consultar, etc.

class Cliente(Resource):
    @role_required(roles=["admin", "cliente"])
    def get(self, id):
        cliente = db.session.query(UsuarioModel).get_or_404(id)
        current_user = get_jwt_identity()
        if cliente.role == 'cliente':
            if current_user ['usuarioId'] == cliente.id or current_user['role'] == 'admin':
                return cliente.to_json()
            else:
                return 'Unauthorized', 401
        else:
            return '', 404
    
    @role_required(roles=["admin", "cliente"])
    def delete(self, id):
        cliente = db.session.query(UsuarioModel).get_or_404(id)
        current_user = get_jwt_identity()
        if cliente.role == 'cliente' and current_user['usuarioId'] == cliente.id:
            try:
                db.session.delete(cliente)
                db.session.commit()
                return '', 204  # codigo 204 significa sin contenido
            except:
                return '', 404
        else:
            return 'Unauthorized', 401

    @role_required(roles=["admin", "cliente"]) 
    def put(self, id):
        cliente = db.session.query(UsuarioModel).get_or_404(id)
        current_user = get_jwt_identity()
        if cliente.role == 'cliente' and current_user['usuarioId'] == cliente.id:
            data = request.get_json().items()
            for key, value in data:
                setattr(cliente, key, value)
            
            try:
                db.session.add(cliente)
                db.session.commit()
                return cliente.to_json(), 201 # Solicitud procesada correctamente
            except:
                return '', 404
        else:
            return 'Unauthorized', 401


class Clientes(Resource):
    @role_required(roles=["admin"])
    def get(self):
        #Filro solo para traer el rol de cliente 
        pagina = 1 # para realizar la paginación
        paginado = 5 # por pagina que me traiga 5 clientes
        clientes = db.session.query(UsuarioModel).filter(UsuarioModel.role == 'cliente')#.all()
        #Estas líneas son para realizar la paginación.
        if request.get_json(silent=True): # Para ignorar el hecho que no se recibe un json
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    pagina = int(value)
                elif key == 'per_page':
                    paginado = int(value)
        clientes = clientes.paginate(page =pagina, per_page=paginado, error_out= True, max_per_page= 10)
        #pagina, por pagina, True que siempre este activa, 15 que sea el limite.
        return jsonify({
            'clientes': [cliente.to_json() for cliente in clientes.items], 
            'total': clientes.total,
            'pages': clientes.pages,
            'page': pagina
        })       
        # return jsonify({
        #     'clientes': [cliente.to_json() for cliente in clientes]
        # })
    
    def post(self):
        cliente = UsuarioModel.from_json(request.get_json())
        #cliente.role = Clientes.role
        db.session.add(cliente)
        db.session.commit()
        return cliente.to_json(), 201
    