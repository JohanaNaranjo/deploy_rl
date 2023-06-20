from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import CompraModel

class Compra(Resource):
    #Para realizr la consulta de una sola compra, por lo que se van a declarar los siguientes metodos.
    def get(self, id):
        compra = db.session.query(CompraModel).get_or_404(id)

        try:
            return compra.to_json()
        except:
            return '', 404
        
#Este metodo es para editar un recurso.
    def put(self, id):
        #Petición de base de datos
        compra = db.session.query(CompraModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            #para setear los objetos
            setattr(compra, key, value)
        try:
            db.session.add(compra)
            db.session.commit()
            return compra.to_json(), 201 # codigo 201 quiere decir que la solicitud fue aceptada y se guardo con exito
        except:
            return '', 404

    #Metodo para borrar un registro
    def delete(self, id):
        compra = db.session.query(CompraModel).get_or_404(id)
        try:
            db.session.delete(compra)
            db.session.commit()
        except:
            return '', 404


#Guardar un compra desde una base de datos, obtener está clase se utiliza para está función, por lo que los compras serán guardados en una variable compras.
class Compras(Resource):
    #Función get para obtener las compras.
    def get(self):
        #Esta instrucción es la misma que se utilizaría en MySql, para la obtener todos los datos.
        #SELECT * FROM compras
        pagina = 1 # para realizar la paginación
        paginado = 3 # por pagina que me traiga 5 compras
        compras = db.session.query(CompraModel)#.all()
        #Estas líneas son para realizar la paginación.
        if request.get_json(silent=True): # Para ignorar el hecho que no se recibe un json
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    pagina = int(value)
                elif key == 'per_page':
                    paginado = int(value)
        compras = compras.paginate(page =pagina, per_page=paginado, error_out= True, max_per_page= 10)
        #pagina, por pagina, True que siempre este activa, 15 que sea el limite.
        return jsonify({
            'compras': [compra.to_json() for compra in compras.items], 
            'total': compras.total,
            'pages': compras.pages,
            'page': pagina
        })


        # return jsonify({
        #     #Esta lista es para que vaya a recorrer todos los compras y los guarde en la lista. los convierte en json y los devuleve en la lista en forma de json
        #     'compras' : [compra.to_json() for compra in compras]
        # })

    def post(self):
        #Esta función la convierte en un objeto python
        compra = CompraModel.from_json(request.get_json()) 
        db.session.add(compra) #Guarda en la base de datos
        db.session.commit() #Base de datos hace commit que es para guardar la inormación que se escribio en la base de datos.
        return compra.to_json(), 201 # Es para que diga que acabo de crear un recurso






