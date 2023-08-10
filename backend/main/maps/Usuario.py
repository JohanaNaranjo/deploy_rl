from marshmallow import Schema, fields, post_load, post_dump
from main.models import UsuarioModel


class UsuarioSchema(Schema):

    id = fields.Integer(dump_only = True)
    nombre = fields.String(required = True)
    apellido = fields.String(required = True)
    email = fields.String(required = True)
    password = fields.String(required = True)
    role = fields.String(required = True)
    telefono = fields.String(required = True)
    fecha_registro = fields.DateTime(required = False) #porque el usuario no la crea se crea por defecto

    @post_load
    def create_usuario(self, data, **kwargs):
        return UsuarioModel(**data)
    
    SKIP_VALUES =['password', 'telefono'] #para que no devuelva estos valores
    @post_dump
    def remove_skip_values(self, data, **kwargs):
        return {
            key: value for key, value in data.items() if key not in self.SKIP_VALUES
        }
    
