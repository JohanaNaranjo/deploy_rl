from marshmallow import Schema, fields, post_load, post_dump
from main.models import CompraModel
from .Usuario import UsuarioSchema

class CompraSchema(Schema):

    id = fields.Integer(dump_only=True)
    fecha_compra = fields.DateTime(required = False) #Porque es por defecto
    usuarioId = fields.Integer(required = True)
    usuario = fields.Nested(UsuarioSchema)

    @post_load
    def create_compra(self, data, **kwargs):
        return CompraModel(**data)
    
    SKIP_VALUES =['usuarioId']
    @post_dump
    def remove_skip_values(self, data, **kwargs):
        return {
            key: value for key, value in data.items() if key  not in self.SKIP_VALUES
        }

