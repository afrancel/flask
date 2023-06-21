#importar
from flask import Flask

#creamos la app. Si ejecutamos este archivo, sera 'main', pero desde otro archivo será 'holamundo.py'
app = Flask(__name__)

#decoradores
@app.route('/') #método para indicar la ruta, se ejecutara lo siguiente cuando llamemos la raíz
def index(): #definimos una función que hace lo siguiente
    return 'flask' #solo retornara este return

#Ahora configuramos el inicio de la app diciendole a flask donde está ubicada la app
#ejecutamos el siguiente código en la consola o gitbash