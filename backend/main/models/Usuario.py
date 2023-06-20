from operator import index
from .. import db
import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):

    #Aqui se empiezan a crear las columnas para la base de datos.
    id = db.Column(db.Integer, primary_key =True)
    nombre = db.Column(db.String(45), nullable = False)
    apellido = db.Column(db.String(45), nullable = False)
    email = db.Column(db.String(45), nullable = False, unique = True, index = True)
    role = db.Column(db.String(45), nullable = False, default = "Cliente")
    telefono = db.Column(db.Integer, nullable = False)
    password = db.Column(db.String(200), nullable = False)
    fecha_registro = db.Column(db.DateTime, default =dt.datetime.now(), nullable = False )
    #cascade es para eliminar las compras de un usuario cuando deja de existir o se elimina, orphan es todas las compras que son de ese usuario
    compras = db.relationship('Compra', back_populates = "usuario", cascade = "all, delete-orphan")

    #Metodos para la contraseña
    #decorador
    #propiedad de clase usuario, va a ser un get de mi contraseña va a ser una propiedad de mi contraseña
    @property
    def plan_password(self):
        raise AttributeError('Password can\'t be read')

    @plan_password.setter
    def plain_password(self, password):
        self.password = generate_password_hash(password)

    #metodo para validar la contraseña
    def validate_pass(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'{self.nombre}'
    
    def to_json(self):
        usuario_json = {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'role': self.role,
            'telefono': self.telefono,
            'fecha': str(self.fecha_registro)
            }
        return usuario_json
    #Cuando se envie un recurtos en formato json desde insomnia, necesito este metodo que nos permite utilizarlo sin utilizar la clase
    @staticmethod
    def from_json(usuario_json):
        id = usuario_json.get('id')
        nombre = usuario_json.get('nombre')
        apellido = usuario_json.get('apellido')
        email = usuario_json.get('email')
        role = usuario_json.get('role')
        telefono = usuario_json.get('telefono')
        password = usuario_json.get('password')
        fecha_registro = usuario_json.get('fecha_registro')
        return Usuario(
            id =id,
            nombre = nombre,
            apellido = apellido,
            email = email,
            role = role,
            telefono = telefono,
            plain_password = password,
            fecha_registro = fecha_registro
        )


        
        
