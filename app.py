#************** IMPORTAMOS ***************#
#ojo, todas las importaciones que yo haga de la misma fuente, pueden ser separadas por coma en un linea,
#solo que las separo para identificar de que trata cada una

from flask import Flask #importamos la libreria
from flask import render_template #importamos el lector de plantillas
from flask import request, redirect #importamos para hacer solicitudes y redirecciones
from flask import session #importamos las sesiones de usuarios
from flaskext.mysql import MySQL #importamos para gestión de BD (Esta es una extensión)
from datetime import datetime #para generar variables de tiempo y trabajar con carga de archivos
import os #necesario para complementar la carga de imagenes

from flask import send_from_directory #para obtener informacion de la imagen

#creamos la app. Si ejecutamos este archivo, sera 'main', pero desde otro archivo será 'holamundo.py'
app = Flask(__name__)

#llave secreta
app.secret_key = "testing"

#configuramos la base de datos
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Site2022Lock'
app.config['MYSQL_DATABASE_DB'] = 'flaskdb'
mysql.init_app(app)

#************** sitio ***************#

@app.route('/') #método para indicar la ruta, se ejecutara cuando llamemos la raíz
def index(): #definimos una función llamada index
    return render_template('sitio/index.html') #indicamos la ruta

@app.route('/imagenes/<imagen>')
def cargar_imagen(imagen):
    print(imagen)
    return send_from_directory(os.path.join('templates/imagenes/'),imagen)

@app.route('/medicos')
def medicos():

    conexion = mysql.connect() #--> conexion inicial de la hoja
    cursor = conexion.cursor() #--> conexion sistema/BD
    cursor.execute("SELECT * FROM medicos;") # --> Selección con cursor la tabla / ojo revisión de nuevo comillas
    lista_medicos = cursor.fetchall()  #--> Ejecuto la sección en la BD
    conexion.commit()  #--> comento como siempre

    return render_template('sitio/medicos.html', medicos=lista_medicos)

@app.route('/nosotros')
def nosotros():
    return render_template('sitio/nosotros.html')

#************** admin ***************#

@app.route('/admin/') #método para indicar la ruta, se ejecutara cuando llamemos la raíz
def admin_index(): #definimos una función llamada index
    return render_template('/admin/index.html') #indicamos la ruta

#CONEXION A BASE DATOS
@app.route('/admin/medicos')
def admin_medicos():

    conexion = mysql.connect() #--> conexion inicial de la hoja
    cursor = conexion.cursor() #--> conexion sistema/BD
    cursor.execute("SELECT * FROM medicos;") # --> Selección con cursor la tabla / ojo revisión de nuevo comillas
    lista_medicos = cursor.fetchall()  #--> Ejecuto la sección en la BD
    conexion.commit()  #--> comento como siempre
    print(medicos) #--> imprimo lo solicitado / cambié de print(conexion) porque se cambió toda la conexión

    return render_template('/admin/medicos.html',medicos=lista_medicos) #--> Conectamos listado con la hoja

@app.route('/admin/nosotros')
def admin_nosotros():
    return render_template('/admin/nosotros.html')

@app.route('/admin/login')
def admin_login():
    return render_template('/admin/login.html')

#LOGIN: RECUPERO EL INGRESO DE DATOS AL FORM DE LOGIN
#VERIFICO SI COINCIDE CON LOS DATOS DE ACCESO
@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    _user = request.form['user_info']
    _pass = request.form['pass_info']
    print(_user,_pass)

    if _user=="admin" and _pass=="admin":
        session['login'] = True
        session['Usuario'] = "Francel"
        return redirect('/admin')

    return render_template('/admin/login.html')

#SESIÓN: DESTRUYO EL INICIO DE SESION AL IR A ESTE LINK
@app.route('/admin/cerrar')
def admin_login_cerrar():
    session.clear()
    return redirect('/admin/login')

#ruta para el request del form de medicos
@app.route('/admin/medicos/guardar',methods=['POST'])
def admin_medicos_guardar():

#CAPTURAR DATOS DEL FORM SIN IMAGEN

    #creo estas variables, que tomarán la info del form de la página e indica que campo del form tomará
    _nombre = request.form['medico_nombre_form']
    _url_linkedin = request.form['medico_url_form']
    _imagen = request.files['medico_imagen_form']

#SUBIR IMAGEN DEL FORM

    #configuración carga y muestra de imagenes
    #Para esto --> importamos from datetime import datetime
    fecha_carga = datetime.now()
    fecha_actual = fecha_carga.strftime('%Y%H%M%S')#--> para mostrar, traer los datos en un formato

    if _imagen.filename!= "":
        imagenNueva = fecha_actual+"_"+ _imagen.filename
        _imagen.save("templates/imagenes/"+imagenNueva)    

#INSERTAR IMAGEN DEL FORM EN BD

    #creo esta variable, para insertar los datos anteriores en la bd
    #01 instrucción SQL con ayuda de workbench
    sql = "INSERT INTO medicos (id, nombre, url, imagen) VALUES (NULL,%s,%s,%s);"
    values = (_nombre,_url_linkedin,imagenNueva) #--> la variable de la imagen cambió

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,values)
    conexion.commit()

    print(_nombre,sep='')
    print(_url_linkedin,sep='')
    print(_imagen)

    return redirect('/admin/medicos')

@app.route('/admin/medicos/borrar', methods = ['POST'])
def admin_medicos_borrar():

    _medico_id_borrar = request.form['medico_id_borrar']


#BORRAR REGISTRO DEL SERVIDOR SIN IMAGEN-->
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT imagen FROM medicos WHERE id = %s;", (_medico_id_borrar))
    medicos = cursor.fetchall()
    conexion.commit()
    print(medicos)

#BORRAR IMAGEN DEL SERVIDOR-->
    #si existe esta imagen, con el click se borra la imagn directo del servidor
    if os.path.exists("templates/imagenes/"+str(medicos[0][0])):
        os.unlink("templates/imagenes/"+str(medicos[0][0]))

#BORRAR REGISTRO DE LA BASE DE DATOS

#<!-- este bloque para borrar la info -->
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM medicos WHERE id = %s;", (_medico_id_borrar))
    conexion.commit()

    return redirect('/admin/medicos')

#************** Instanciamos ********#
if __name__ == '__main__':
    app.run(debug=True)