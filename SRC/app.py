from datetime import datetime
from flask import Flask
from flask import render_template
from flask import request, redirect
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mypass'
app.config['MYSQL_DATABASE_DB'] = 'alumnos'
app.config['MYSQL_DATABASE_PORT'] = 3306

mysql.init_app(app)

@app.route('/')
def index():
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "SELECT * FROM alumnos;"
    cursor.execute(sql)

    alumnos = cursor.fetchall()

    conn.commit()
    print(*alumnos)

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
    print(now)
    tiempo = now.strftime("%Y%H%M%S")
    print(tiempo)

    if _foto.filename != '':
        nuevoNombreFoto = tiempo + '_' + _foto.filename
        _foto.save("uploads/" + nuevoNombreFoto)

    sql = "INSERT INTO alumnos (nombre, apellido, mail, horarios, cel, foto) values (%s, %s, %s, %s, %s, %s);"
    datos = (_nombre, _apellido, _mail, _horarios, _celular, _foto.filename)

    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True) 
