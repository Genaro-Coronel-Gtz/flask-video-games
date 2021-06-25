https://nordicapis.com/how-to-create-an-api-using-the-flask-framework/
https://stackabuse.com/integrating-mongodb-with-flask-using-flask-pymongo
https://docs.mongodb.com/guides/server/read/

#para hacerlo con sqlite
https://stackabuse.com/building-a-todo-app-with-flask-in-python
https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/

https://plataforma.josedomingo.org/pledin/cursos/flask/curso/u22/index.html

Hacer los tutoriales con sqlite y en flask con sqlachemy

* Investigar si en express se puede utilizar sqlite
* Utilizar en todos los proyectos jwt para la autenticacion


sqlite jwt -> https://geekflare.com/es/securing-flask-api-with-jwt/
jwt flas avanzado -> https://codeburst.io/jwt-authorization-in-flask-c63c1acf4eeb (como agregar acciones a los modelos, .save_to_db [ejemplo], try y atch si falla al guardar en la bd.)
https://www.geeksforgeeks.org/using-jwt-for-user-authentication-in-flask/

Backends:
 * Laravel (php)
 * Slim 3.0 (php)
 * Express (node)
 * Rails (ruby)
 * Flask (python)
 * Django (python)

 Frontend:
  * ReactJs
  * Vue
  * Angular
  * Ember
  * Flutter


  investigar -> Flask-RESTful==0.3.8????

### crear virtaulenv

pip3 install virtualenv -> si no se tiene instalador

crear 
virtualenv .
activar
source bin/activate

instalar requirements
pip3 install -r requirements.txt

eliminar virtual env
rm -r bin include lib lib64 pyvenv.cfg share -> omitir lib64 y share


* Al crear un autor tiene validacion que el nombre del libro no exista!


*doc jwt -> https://pyjwt.readthedocs.io/en/stable/


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///library.db' 
# /// 3 slashes for relative path
# //// 4 slashes for absolute path


## relationships

https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/


### Crear bd
from app import db
db.create_all()


#GrapQl

https://www.twilio.com/blog/graphql-api-python-flask-ariadne


   genre=data['genre'], company_id=1, user_id=current_user.id)


   Flask-PyMongo -> no es necesaria esta libreria para el proyecto de videojuegos