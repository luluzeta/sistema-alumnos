from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime
import os

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mypass'
app.config['MYSQL_DATABASE_DB'] = 'alumnos'
#app.config['MYSQL_DATABASE_PORT'] = 3306

UPLOADS = os.path.join('SRC/uploads')
app.config['UPLOADS'] = UPLOADS # Guardamos la ruta como un valor en la app

mysql.init_app(app)

@app.route('/')
def index():
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "SELECT * FROM alumnos;"
    cursor.execute(sql)

    alumnos = cursor.fetchall()

    conn.commit()

    return render_template('alumnos/index.html', alumnos=alumnos)

@app.route('/create')
def create():
    return render_template('alumnos/create.html')

@app.route('/store', methods=["POST"])
def store():
    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _mail = request.form['txtMail']
    _horarios = request.form['txtHorario']
    _celular = request.form['txtCel']
    _foto = request.files['txtFoto']

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _foto.filename != '':
        nuevoNombreFoto = tiempo + '_' + _foto.filename
        _foto.save("SRC/uploads/" + nuevoNombreFoto)

    sql = "INSERT INTO alumnos (nombre, apellido, mail, horarios, cel, foto) values (%s, %s, %s, %s, %s, %s);"
    datos = (_nombre, _apellido, _mail, _horarios, _celular, nuevoNombreFoto)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    sql = "SELECT foto FROM alumnos WHERE id = (%s);"
    datos = [id]

    try:
        os.remove(os.path.join(app.config['UPLOADS'], nombreFoto[0]))
    except:
        pass

    sql = "DELETE FROM alumnos WHERE id = (%s);"

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

    return redirect('/') 


@app.route('/modify/<int:id>')
def modify(id):
    sql = f'SELECT * FROM alumnos WHERE id={id}'
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
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

    datos = (_nombre, _apellido, _mail, _horarios, _celular, id)

    conn = mysql.connect()
    cursor = conn.cursor()
     
    if _foto.filename != '':
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        nuevoNombreFoto = tiempo + '_' + _foto.filename
        _foto.save("SRC/uploads/" + nuevoNombreFoto)

        sql = f'SELECT foto FROM alumnos WHERE id={id}'  
        cursor.execute(sql)

        nombreFoto = cursor.fetchone()[0]
        try:
            os.remove(os.path.join(app.config['UPLOADS'], nombreFoto))
        except:
            pass

        sql = f'UPDATE alumnos SET foto="{nuevoNombreFoto}" WHERE id={id}'
        cursor.execute(sql)
        conn.commit()
    
    sql = f'UPDATE alumnos SET nombre="{_nombre}", apellido="{_apellido}", mail="{_mail}", horarios="{_horarios}", cel="{_celular}" WHERE id={id}'
    cursor.execute(sql)
    conn.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True) 

