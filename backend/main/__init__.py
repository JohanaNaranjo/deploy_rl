import os
from flask import Flask
from dotenv import load_dotenv

#importo el módulo para crear la api-rest
from flask_restful import Api

#Importo el módulo para conectarme a una base de datos MySQL.
from flask_sqlalchemy import SQLAlchemy

#Importo el módulo para trabajara con JWT (Json Web Tockens)
"""Json wb tockens
Es un estandar para la creacion de tockens de acceso basada en json, evita guardar de sesion o sesiones al lado del servidor, evita guardar datos en el servidor.
Permiten autentificar un usuario por medio de api-rest

Como funciona

El cliente envia sus credenciales al servidor, el servidor genera un Json Web tocken y se lo devuelve al cliente.
El cliente guarda localmente el tocken, lo guarda en el navegador en forma de cookie. (Se guarda en el navegador)
Cabecera, contenido y firma son las partes del tocken, no se pueden guardar datos sensibles, como contraseñas

"""
from flask_jwt_extended import JWTManager
#Importo el modulo para trabajar el envio del mail
from flask_mail import Mail


api = Api()

#Clase de Sql Alchemy para conectar a base de datos
db = SQLAlchemy()

#Para trabajar los JWT
jwt = JWTManager()

#Para enviar los mail
mailsender = Mail()

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
    import main.controllers as controllers

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
    
    api.add_resource(controllers.CompraController, '/compra-controller/<id>')
    api.add_resource(controllers.ComprasController, '/compras-controller')


    #Agregar el objeto a la app
    api.init_app(app)

    #Configurar el JWT
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES"))
    jwt.init_app(app)

    #blueprints
    from main.auth import routes
    app.register_blueprint(auth.routes.auth)
    from main.mail import functions
    app.register_blueprint(mail.functions.mail)

    #Configurar mail
    app.config['MAIL_HOSTNAME'] = os.getenv('MAIL_HOSTNAME')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')    
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['FLASKY_MAIL_SENDER'] = os.getenv('FLASKY_MAIL_SENDER')

    mailsender.init_app(app)

    return app

