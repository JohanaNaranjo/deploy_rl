from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioModel

class Usuario(Resource):
    #Obtener usuarios en especifico
    
    def get(self, id):
        #El comando equivalente en sql de este comando es el siguiente:
        #SELECT * FROM usuario WHERE usuario.id = <id>;
        usuario = db.session.query(UsuarioModel).get_or_404(id)

        #Este try es por si no existe el usuario que se ingrese en la URL no caiga el servidor y capture el error, entonces en el try retorna el usuario si existe y en el except muestra el mensaje de error
        try:
            return usuario.to_json()
        except:
            return 'Resource no found', 404
        
    #Este metodo es para editar un recurso.
    def put(self, id):
        #Petición de base de datos
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            #para setear los objetos
            setattr(usuario, key, value)
        try:
            db.session.add(usuario)
            db.session.commit()
            return usuario.to_json(), 201 # codigo 201 quiere decir que la solicitud fue aceptada yy se guardo con exito
        except:
            return '', 404

    #Metodo para borrar un registro
    def delete(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        try:
            db.session.delete(usuario)
            db.session.commit()
        except:
            return '', 404

class Usuarios(Resource):
    #Función get para obtener los usuarios.
    def get(self):

        pagina = 1 # para realizar la paginación
        paginado = 5 # por pagina que me traiga 5 usuarios
        usuarios = db.session.query(UsuarioModel)#.all()
        #Estas líneas son para realizar la paginación.
        if request.get_json(silent=True): # Para ignorar el hecho que no se recibe un json
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    pagina = int(value)
                elif key == 'per_page':
                    paginado = int(value)
        usuarios = usuarios.paginate(page =pagina, per_page=paginado, error_out= True, max_per_page= 10)
        #pagina, por pagina, True que siempre este activa, 15 que sea el limite.
        return jsonify({
            'usuarios': [usuario.to_json() for usuario in usuarios.items], 
            'total': usuarios.total,
            'pages': usuarios.pages,
            'page': pagina
        })
        #Esta instrucción es la misma que se utilizaría en MySql, para la obtener todos los datos.
        #SELECT * FROM Productos
        # return jsonify({
        #     #Esta lista es para que vaya a recorrer todos los usuarios y los guarde en la lista. los convierte en json y los devuleve en la lista en forma de json
        #     'usuarios' : [usuario.to_json() for usuario in usuarios]
        # })





