import os
from flask import Flask
from dotenv import load_dotenv

#importo el módulo para crear la api-rest
from flask_restful import Api

#Importo el módulo para conectarme a una base de datos MySQL.
from flask_sqlalchemy import SQLAlchemy

api = Api()

#Clase de Sql Alchemy para conectar a base de datos
db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    #Cargo las variables de entorno.
    load_dotenv()

    #Cargo varibales de entorno
    PATH = os.getenv("DATABASE_PATH")
    DB_NAME = os.getenv("DATABASE_NAME")
    if not os.path.exists(f'{PATH}{DB_NAME}'):
        os.chdir(f'{PATH}')
        file = os.open(f'{DB_NAME}', os.O_CREAT)
    #Para que me mande la base de datos que cambios se han hecho en todo momento para que los trackee en todo momento.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{PATH}{DB_NAME}'
    db.init_app(app) #Iniciar la app principal
    


    import main.resources as resources
    #Ubicación del recurso para ser obtenido.
    api.add_resource(resources.ClientesResource, '/clientes')
    api.add_resource(resources.ClienteResource, '/cliente/<id>')
    api.add_resource(resources.UsuariosResource, '/usuarios')
    api.add_resource(resources.UsuarioResource, '/usuario/<id>')
    api.add_resource(resources.ComprasResource, '/compras')
    api.add_resource(resources.CompraResource, '/compra/<id>')
    api.add_resource(resources.ProductosResource, '/productos')
    api.add_resource(resources.ProductoResource, '/producto/<id>')
    api.add_resource(resources.ProductosComprasResource, '/productos-compras')
    api.add_resource(resources.ProductoCompraResource, '/producto-compra/<id>')

    #Agregar el objeto a la app
    api.init_app(app)

    return app

