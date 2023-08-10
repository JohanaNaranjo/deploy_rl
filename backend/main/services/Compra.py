#Son las entidades software que se encargan de la lógica de la aplicación.

from main.repositories import CompraRepository

compra_repository = CompraRepository()

class CompraService:

    def obtener_compra_con_descuento(self ,id):
        compra = compra_repository.find_one(id)
        #podria agregar un tipo de lógica para calcular el descuento
        #compra.total = compra.total - {compra.total * 0.1}
        return compra

    def agregar_compra(self, compra):
        #Agrgar l´gica antes de guardar fisicamente la com´pra en la db
        compra = compra_repository.create(compra)
        return compra