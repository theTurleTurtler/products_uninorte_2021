from flask import Flask, session
from flask import render_template as render
from flask import redirect, url_for
from flask import request
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

from flask.helpers import flash
app = Flask(__name__)

@app.route("/")
def index():
    return render("index.html")


@app.route("/califications/<product_id>", methods=["GET", "POST"])
def getCalifications(product_id):
    return render("califications.html")

@app.route("/edit_perfil")
def edit_perfil():
    return render("EditarPerfil.html")









""" roberto posada empezo aqui """
def sql_connection():
    con = sqlite3.connect('agenda.db')
    return con

@app.route("/agregar_producto")
def agregar():
    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        precio = request.form['precio']
        comentario = request.form['comentario']
        con = sql_connection()
        cur = con.cursor()
        consulta = "INSERT INTO producto (codigo, nombre, precio, comentario) VALUES (?,?,?,?)"
        cur.execute(consulta, [codigo, nombre, precio, comentario])
        con.commit()
       
        flash('Producto Agregado Exitosamente')
        return render("index.html")
    
@app.route('/edit_product/<id_producto>', methods=['GET', 'POST'])
def edit_contact(id_producto):
    con = sql_connection()
    cur = con.cursor()
    consulta = "SELECT * FROM producto WHERE id_producto=?"
    cur = cur.execute(consulta, [id_producto])
    data = cur.fetchone()
    cur.close()
    return render('edit_product.html', contacts=data)

@app.route('/update/<id_producto>', methods=['GET', 'POST'])
def update_contact(id_producto):
    if request.method == 'POST':
        con = sql_connection()
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        precio = request.form['precio']
        comentario = request.form['comentario']
        
        cur = con.cursor()
        consulta = "UPDATE producto SET codigo = ?, nombre = ?, precio = ?, comentario = ? WHERE id_producto = ?"
        cur.execute(consulta, [codigo, nombre, precio, comentario, id_producto])
        con.commit()
        
        flash('Producto Actualizado Exitosamente')
        return redirect(url_for('index'))
 
@app.route('/delete_product/<int:id_producto>', methods=['GET', 'POST'])
def delete_contact(id_producto):
    con = sql_connection()
    cur = con.cursor()
    cur.execute('DELETE FROM producto WHERE id_producto={0}'.format(id_producto))
    con.commit()
    
    flash('Producto Eliminado Exitosamente')
    return redirect(url_for('index'))




@app.route("/producto")
def producto():
    return render("Producto.html")



@app.route( '/registro', methods=('GET', 'POST') )
def registro():
    try:
        if request.method == 'POST':
            
            name= request.form['nombre']
            username = request.form['username']
            password = request.form['password']
            email = request.form['correo']
            
            
            password = generate_password_hash(password)
            con = sql_connection()
            cur = con.cursor()
            cur.executescript("INSERT INTO usuario (nombre, usuario, correo, contraseña) VALUES ('%s', '%s', '%s', '%s')" % (name, username, email, password,))
            con.commit()
            flash('Usuario creado en la BD')
                           
            return render( 'Login.html' )
        return render( 'Registro.html' )
    except:
        return render( 'Registro.html' )



@app.route("/verificacion")
def verificacion():
    return render("Verificacion.html")

@app.route( '/login', methods=('GET', 'POST') )
def login():
    try:
        if request.method == 'POST':
            con = sql_connection()
            error = None
            username = request.form['username']
            password = request.form['password']

            if not username:
                error = 'Debes ingresar el usuario'
                flash( error )
                return render( 'Login.html' )

            if not password:
                error = 'Contraseña requerida'
                flash( error )
                return render( 'Login.html' )
           
            cur = con.execute(
                'SELECT * FROM usuario WHERE usuario = ?', (username,)
            ).fetchone()

            print(cur[0])
            if cur is None:
                error = 'Usuario o contraseña inválidos'
            else:
                if check_password_hash(cur[4], password):
                    session.clear()
                    session['user_id'] = cur[0]
                    
                    return redirect( 'message' )
                else:
                    error = 'Usuario o contraseña inválidos'
            flash( error )
        return render( 'Login.html' )
    except:
        return render( 'Login.html' )

@app.route("/mapa")
def mapa():
    return render("Mapa.html")


@app.route("/perfil")
def perfil():
    return render("Perfil.html")

@app.route("/codigo")
def codigo():
    return render("Codigo.html")
if __name__ == "__main__":
        app.run(debug=True)
