from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ProductoModel
from main.auth.decorators import role_required
from flask_jwt_extended import get_jwt_identity

class Producto(Resource):
    #Obtener productos en especifico
    
    def get(self, id):
        #El comando equivalente en sql de este comando es el siguiente:
        #SELECT * FROM producto WHERE producto.id = <id>;
        producto = db.session.query(ProductoModel).get_or_404(id)

        #Este try es por si no existe el producto que se ingrese en la URL no caiga el servidor y capture el error, entonces en el try retorna el producto si existe y en el except muestra el mensaje de error
        try:
            return producto.to_json()
        except:
            return 'Resource no found', 404
        
    #Este metodo es para editar un recurso.
    @role_required(roles=["admin"])
    def put(self, id):
        #Petición de base de datos
        producto = db.session.query(ProductoModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            #para setear los objetos
            setattr(producto, key, value)
        try:
            db.session.add(producto)
            db.session.commit()
            return producto.to_json(), 201 # codigo 201 quiere decir que la solicitud fue aceptada yy se guardo con exito
        except:
            return '', 404

    #Metodo para borrar un registro
    @role_required(roles=["admin"])
    def delete(self, id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        try:
            db.session.delete(producto)
            db.session.commit()
        except:
            return '', 404


#Guardar un producto desde una base de datos, obtenero está clase se utiliza para está función, por lo que los productos serán guardados en una variable productos.
class Productos(Resource):
    
    #Función get para obtener los productos.
    def get(self):
        pagina = 1 # para realizar la paginación
        paginado = 5 # por pagina que me traiga 5 productos
        productos = db.session.query(ProductoModel)#.all()
        #Estas líneas son para realizar la paginación.
        if request.get_json(silent=True): # Para ignorar el hecho que no se recibe un json
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    pagina = int(value)
                elif key == 'per_page':
                    paginado = int(value)
        productos = productos.paginate(page =pagina, per_page=paginado, error_out= True, max_per_page= 10)
        #pagina, por pagina, True que siempre este activa, 15 que sea el limite.
        return jsonify({
            'productos': [producto.to_json() for producto in productos.items], 
            'total': productos.total,
            'pages': productos.pages,
            'page': pagina
        })

        #Esta instrucción es la misma que se utilizaría en MySql, para la obtener todos los datos.
        #SELECT * FROM Productos
    #    return jsonify({
    #         #Esta lista es para que vaya a recorrer todos los productos y los guarde en la lista. los convierte en json y los devuleve en la lista en forma de json
    #         'productos' : [producto.to_json() for producto in productos]
    #     })

    @role_required(roles=["admin"])
    def post(self):
        #Esta función la convierte en un objeto python
        producto = ProductoModel.from_json(request.get_json()) 
        db.session.add(producto) #Guarda en la base de datos
        db.session.commit() #Base de datos hace commit que es para guardar la inormación que se escribio en la base de datos.
        return producto.to_json() # Es para que diga que acabo de crear un recurso




