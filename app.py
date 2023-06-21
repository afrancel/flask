#importar
from flask import Flask
from flask import render_template

#creamos la app. Si ejecutamos este archivo, sera 'main', pero desde otro archivo será 'holamundo.py'
app = Flask(__name__)

#************** index ***************#
#decoradores
@app.route('/') #método para indicar la ruta, se ejecutara cuando llamemos la raíz
def index(): #definimos una función llamada index
    return render_template('sitio/index.html') #indicamos la ruta

#Instanciamos
if __name__ == '__main__':
    app.run(debug=True)