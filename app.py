from os import name
from flask import Flask, flash, redirect, url_for, session, g, make_response, abort
from flask import render_template as render
from flask import redirect, url_for
from flask import request
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


# -------------------------------------------------------

import os
from werkzeug.datastructures import Authorization
from os import getenv

import utils
from db import get_db
import pathlib

import requests

from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
# -------------------------------------------------------

from flask.helpers import flash
app = Flask(__name__)


# @app.route("/")
# def index():
#     return render("index.html")

@app.route( '/' )
def index():
    if g.user:
        return redirect( url_for( 'producto' ) )
    return render( 'Login.html' )





@app.route("/califications/<product_id>", methods=["GET", "POST"])
def getCalifications(product_id):
    return render("califications.html")

@app.route("/edit_perfil")
def edit_perfil():
    return render("EditarPerfil.html")

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




@app.route( '/Registro', methods=('GET', 'POST') )
def registro():
    try:
        if request.method == 'POST':
      
            name= request.form['nombre']
            apellido = request.form['apellido']
            password = request.form['password']
            email = request.form['correo']
            error = None
            db = get_db()  
            
            if not utils.isUsernameValid( apellido ):
                error = "El apellido es necesario"
                flash( error )
                return render( 'Registro.html' )


            if not utils.isPasswordValid( password ):
                error = 'La contraseña debe contenir al menos una minúscula, una mayúscula, un número y 8 caracteres'
                flash( error )
                return render( 'Registro.html' )

            if not utils.isEmailValid( email ):
                error = 'El correo debe contener @'
                flash( error )
                return render( 'Registro.html' )


            cur = db.execute('SELECT * FROM usuario WHERE correo = ?', (email,)).fetchone()
          
            
            
            if cur is None:
                error = "El correo no existe"
                password = generate_password_hash(password) 
                db = get_db()       
                cur = db.cursor()   
                cur.executescript("INSERT INTO usuario (nombre, apellido, correo, contraseña) VALUES ('%s', '%s', '%s', '%s')" % (name, apellido, email, password,)) 
                db.commit()
                flash('Registrado exitosamente')

                return render('Login.html')
            else:
                
                error ="El correo ya existe"
        
            flash(error)
        

        return render( 'Registro.html' )
        
    except:
        return render( 'Registro.html' )









@app.route('/Login', methods=('GET', 'POST'))
def login():
   
    try:
        if request.method == 'POST':
            db = get_db()       
            error = None
            username = request.form['correoEmail']
            password = request.form['password']

            
            if not username:
                error = 'El correo electronico es requerido'
                flash(error)
                return render('Login.html')

            if not password:
                error = 'La contraseña es requerida'
                flash(error)
                return render('Login.html')


            cur = db.execute('SELECT * FROM usuario WHERE correo = ?', (username,)).fetchone()
          
            
            """ print(cur[0])
            print(cur[1])
            print(cur[2])
            print(cur[3])
            print(cur[4]) """
            
            if cur is None:
                error = "El correo no existe"
            else:
                
                if check_password_hash(cur['contraseña'], password): 
                    session.clear()
                    session['user_id'] = cur[0] 
                    
                    resp = make_response( redirect( url_for('producto')))
                    resp.set_cookie('correoEmail', username )
                    return resp
                    
                else:
                    error ="La contraseña no es valida"
                    

            flash(error)
        
        return render('Login.html')
    except:
        return render('Login.html')



@app.before_request
def logged():
    user_id = session.get( 'user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM usuario WHERE id=?', (user_id,)).fetchone()
        
    print(g.user)



@app.route('/Google', methods=('GET', 'POST'))
def goo():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)




GOOGLE_CLIENT_ID = "494550765014-uj9nn1n20g87p59ov6e59tkfong98sit.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")


flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)
    

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"




@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)
    
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    # return id_info

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    flash(id_info.get("name"))
    flash(id_info.get("email"))
    return redirect("/Product")


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function()
    
    return wrapper



@app.route('/Producto', methods=['GET', 'POST'])
def producto(): 
    if g.user:
        db = get_db()       
        # error = None
        cookie = request.cookies.get('correoEmail')  # Obtener, leer cookie
        print(cookie)
        cur = db.execute('SELECT * FROM usuario WHERE correo = ?', (cookie,)).fetchone()
        #consulta
        flash(cur[1] + " " + cur[2])
        flash(cookie)
    else:
        return render('Producto.html')
    return render('Producto.html')

@app.route('/Product', methods=['GET', 'POST'])
@login_is_required
def product():
    return render('Producto.html')


@app.route( '/logout')
def logout():
    session.clear()
    return redirect(url_for('login')) # o return redirect("/")


@app.route('/Mapa')
def mapa():
    return render("Mapa.html")


@app.route("/verificacion")
def verificacion():
    return render("Verificacion.html")


@app.route("/perfil")
def perfil():
    return render("Perfil.html")

@app.route("/codigo")
def codigo():
    return render("Codigo.html")



if __name__ == "__main__":
        app.run(debug=True)
