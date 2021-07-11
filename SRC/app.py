from flask import Flask
from flask import render_template
from flask.wrappers import Request
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'hollywood01!'
app.config['MYSQL_DATABASE_DB'] = 'alumnos'

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
    _nombre = Request.form['txtNombre']
    _apellido = Request.form['txtApellido']
    _mail = Request.form['txtMail']
    _horarios = Request.form['txtHorarios']
    _celular = Request.form['txtCelular']
    _foto = Request.files['txtFoto']

    sql = "INSERT INTO alumnos (nombre, apellido, mail, horarios, cel, foto) values (%s, %s, %s, %s, %s);"
    datos = (_nombre, _apellido, _mail, _horarios, _celular, _foto.filename)

    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return render_template('alumnos/index.html')


if __name__ == '__main__':
    app.run(debug=True) 
