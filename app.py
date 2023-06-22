#************** base ***************#

#importar
from flask import Flask
from flask import render_template

#creamos la app. Si ejecutamos este archivo, sera 'main', pero desde otro archivo será 'holamundo.py'
app = Flask(__name__)


#************** Instanciamos ********#
if __name__ == '__main__':
    app.run(debug=True)


#************** sitio ***************#

@app.route('/') #método para indicar la ruta, se ejecutara cuando llamemos la raíz
def index(): #definimos una función llamada index
    return render_template('sitio/index.html') #indicamos la ruta

@app.route('/medicos')
def medicos():
    return render_template('sitio/medicos.html')

@app.route('/nosotros')
def nosotros():
    return render_template('sitio/nosotros.html')

#************** admin ***************#

@app.route('/admin/') #método para indicar la ruta, se ejecutara cuando llamemos la raíz
def admin_index(): #definimos una función llamada index
    return render_template('/admin/index.html') #indicamos la ruta

@app.route('/admin/medicos')
def admin_medicos():
    return render_template('/admin/medicos.html')

@app.route('/admin/nosotros')
def admin_nosotros():
    return render_template('/admin/nosotros.html')