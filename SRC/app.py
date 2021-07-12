from flask import Flask
from flask import render_template
from flask import request
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'hollywood01!'
app.config['MYSQL_DATABASE_DB'] = 'alumnos'
app.config['MYSQL_DATABASE_PORT'] = 3306

mysql.init_app(app)

@app.route('/')
def index():
    # conn = mysql.connect()
    # cursor = conn.cursor()
    # sql = 'insert into alumnos (nombre, mail, foto) values ("Juan", "juan.gmail@gmail.com", "fotojuan.jpg");'
    # cursor.execute(sql)

    # conn.commit()

    return render_template('alumnos/index.html')

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

    sql = "INSERT INTO alumnos (nombre, apellido, mail, horarios, cel, foto) values (%s, %s, %s, %s, %s, %s);"
    datos = (_nombre, _apellido, _mail, _horarios, _celular, _foto.filename)

    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return render_template('alumnos/index.html')


if __name__ == '__main__':
    app.run(debug=True) 
