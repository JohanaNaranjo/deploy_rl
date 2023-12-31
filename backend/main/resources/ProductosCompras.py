from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ProductoCompraModel

class ProductoCompra(Resource):
    #Obtener productos en especifico
    
    def get(self, id):
        #El comando equivalente en sql de este comando es el siguiente:
        #SELECT * FROM productocompra WHERE productocompra.id = <id>;
        productocompra = db.session.query(ProductoCompraModel).get_or_404(id)

        #Este try es por si no existe el productocompra que se ingrese en la URL no caiga el servidor y capture el error, entonces en el try retorna el productocompra si existe y en el except muestra el mensaje de error
        try:
            return productocompra.to_json()
        except:
            return 'Resource no found', 404
        
    #Este metodo es para editar un recurso.
    def put(self, id):
        #Petición de base de datos
        productocompra = db.session.query(ProductoCompraModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            #para setear los objetos
            setattr(productocompra, key, value)
        try:
            db.session.add(productocompra)
            db.session.commit()
            return productocompra.to_json(), 201 # codigo 201 quiere decir que la solicitud fue aceptada yy se guardo con exito
        except:
            return '', 404

    #Metodo para borrar un registro
    def delete(self, id):
        productocompra = db.session.query(ProductoCompraModel).get_or_404(id)
        try:
            db.session.delete(productocompra)
            db.session.commit()
        except:
            return '', 404

class ProductosCompras(Resource):
    #Función get para obtener los productoscompras.
    def get(self):
        pagina = 1 # para realizar la paginación
        paginado = 5 # por pagina que me traiga 5 productoscompras
        productoscompras = db.session.query(ProductoCompraModel)#.all()
        #Estas líneas son para realizar la paginación.
        if request.get_json(silent=True): # Para ignorar el hecho que no se recibe un json
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    pagina = int(value)
                elif key == 'per_page':
                    paginado = int(value)
        productoscompras = productoscompras.paginate(page =pagina, per_page=paginado, error_out= True, max_per_page= 10)
        #pagina, por pagina, True que siempre este activa, 15 que sea el limite.
        return jsonify({
            'productoscompras': [productocompra.to_json() for productocompra in productoscompras.items], 
            'total': productoscompras.total,
            'pages': productoscompras.pages,
            'page': pagina
        })
        #Esta instrucción es la misma que se utilizaría en MySql, para la obtener todos los datos.
        #SELECT * FROM Productoscompras
        # return jsonify({
        #     #Esta lista es para que vaya a recorrer todos los productoscompras y los guarde en la lista. los convierte en json y los devuleve en la lista en forma de json
        #     'productoscompras' : [productocompra.to_json() for productocompra in productoscompras]
        # })

    def post(self):
        #Esta función la convierte en un objeto python
        productocompra = ProductoCompraModel.from_json(request.get_json()) 
        db.session.add(productocompra) #Guarda en la base de datos
        db.session.commit() #Base de datos hace commit que es para guardar la inormación que se escribio en la base de datos.
        return productocompra.to_json(), 201 # Es para que diga que acabo de crear un recurso






