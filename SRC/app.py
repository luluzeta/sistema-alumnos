from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from flaskext.mysql import MySQL
from datetime import datetime
import os

from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mypass'
app.config['MYSQL_DATABASE_DB'] = 'alumnos'
app.config['SECRET_KEY'] = 'codoacodo'

UPLOADS = os.path.join('SRC/uploads')
app.config['UPLOADS'] = UPLOADS # Guardamos la ruta como un valor en la app

mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor(cursor=DictCursor)

@app.route('/userpicture/<path:nombreFoto>')
def uploads(nombreFoto):    
    return send_from_directory(os.path.join('uploads'), nombreFoto)

@app.route('/')
def index():

    sql = "SELECT * FROM alumnos;"
    cursor.execute(sql)

    alumnos = cursor.fetchall()

    conn.commit()

    return render_template('alumnos/index.html', alumnos=alumnos)

@app.route('/alumnos/crear', methods=["GET", "POST"])
def alta_alumno():
    if request.method == "GET":
        return render_template('alumnos/create.html')
    elif request.method == "POST":
        _nombre = request.form['txtNombre']
        _apellido = request.form['txtApellido']
        _mail = request.form['txtMail']
        _horarios = request.form['txtHorario']
        _celular = request.form['txtCel']
        _foto = request.files['txtFoto']

        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")

        #nuevoNombreFoto = None
        if _nombre == '' or _mail == '' or _horarios == '':
            flash('El nombre, el correo y el horario son obligatorios.')
            return redirect(url_for('alta_alumno'))
        
        if _foto.filename != '':
            nuevoNombreFoto = tiempo + '_' + _foto.filename
            _foto.save("SRC/uploads/" + nuevoNombreFoto)
        
        sql = "INSERT INTO alumnos (nombre, apellido, mail, horarios, cel, foto) values (%s, %s, %s, %s, %s, %s);" ####TODO TIENE QUE TENER ESTE FORMATO MODIFICAR
        datos = (_nombre, _apellido, _mail, _horarios, _celular, nuevoNombreFoto)

        cursor.execute(sql, datos)
        conn.commit()

        return redirect('/')

@app.route('/borrar/<int:id>')
def delete(id):    
    
    sql = "SELECT foto FROM alumnos WHERE id = (%s);" ####TODO TIENE QUE TENER ESTE FORMATO MODIFICAR
    datos = [id]
    cursor.execute(sql,datos)

    nombreFoto = cursor.fetchone()[0]
    print(nombreFoto)

    try:
        os.remove(os.path.join(app.config['uploads'], nombreFoto)) ########NO ME BORRA LA FOTO
        
    except:
        pass

    sql = "DELETE FROM alumnos WHERE id = (%s);"
    datos = [id]
    cursor.execute(sql, datos)
    
    conn.commit()

    return redirect('/') 


@app.route('/modificar/<int:id>')
def modify(id):
    sql = "SELECT * FROM alumnos WHERE id=(%s)"
    datos = [id]
    cursor.execute(sql, datos)
    alumnos = cursor.fetchone()
    conn.commit()
    return render_template('alumnos/edit.html', alumno=alumnos) 

@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _mail = request.form['txtMail']
    _horarios = request.form['txtHorario']
    _celular = request.form['txtCel']
    _foto = request.files['txtFoto']
    id = request.form['txtId']
     
    if _foto.filename != '':
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        nuevoNombreFoto = tiempo + '_' + _foto.filename
        _foto.save("SRC/uploads/" + nuevoNombreFoto)

        sql = "SELECT foto FROM alumnos WHERE id=(%s);" 
        datos=[id]
        cursor.execute(sql, datos)
        conn.commit()

        nombreFoto = cursor.fetchone()[0]
        
        try:
            os.remove(os.path.join(app.config['UPLOADS'], nombreFoto))
        except:
            pass

        sql = "UPDATE alumnos SET foto=(%s) WHERE id=(%s);"
        datos = (nuevoNombreFoto, id)
        cursor.execute(sql, datos)
        conn.commit()
    
    sql = "UPDATE alumnos SET nombre=(%s), apellido=(%s), mail=(%s), horarios=(%s), cel=(%s) WHERE id = (%s)"
    datos = (_nombre, _apellido, _mail, _horarios, _celular, id)
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True) 

