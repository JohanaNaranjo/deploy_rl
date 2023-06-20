from main import create_app, db
import os

app = create_app()

#permite acceder a las variables de la aplicación en cualquier parte del sistema
app.app_context().push()

if __name__ == '__main__':

    #Para crear todas las tablas de las bases de datos se realiza el siguiente comando, db ya se sabe es la base de datos.

    db.create_all()

    #Va a permitir realizar un refresco rápido, para cualquier cambio que se realice en la aplicación y no se tenga que reiniciar el servidor, sino que se va a refrescar automaticamente cada vez que tenga un cambio nuevo.
    app.run(port = os.getenv("PORT"), debug=True)
