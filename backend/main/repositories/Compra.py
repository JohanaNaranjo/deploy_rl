from .. import db
from main.models import CompraModel

# con este archivo se puede llegar a hacer todo lo qhe se hizo en la carpeta resources pero con menos lineas de codigo, asi de esta manera se tiene un código menos robusto pero que tiene la misma funcionalidad, esto ya es a nivel profesional


#En el repository no se guarda nada de lógica, soólo conexión con la base de datos
class CompraRepository:

    __modelo = CompraModel

    @property
    def modelo(self):
        return self.__modelo
    
    def find_one(self, id):
        object = db.session.query(self.modelo).get(id)
        return object

    def find_all(self, id):
        objects = db.session.query(self.modelo).all()
        return objects
    
    def create(self, object):
        db.session.add(object)
        db.session.commit()
        return object
    
    def update(self, object):
        return self.create(object)
    
    def delete(self, id):
        object = self.find_one(id)
        db.session.delete(object)
        db.session.commit()
        return object