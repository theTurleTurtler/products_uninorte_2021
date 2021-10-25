from os import name
from app import *

@app.cli.command("crear_datos_iniciales")
def crear_datos_iniciales():
    db.init_app(app)
    ## crea el usuario si no existe, y, si existe, solo lo retorna.
    u1 = User.get_or_create(firstName="Jackie", lastName="Chan", email="jackieChan@karate.com", password="password", role="final")
    u2 = User.get_or_create(firstName="Sir William", lastName="Wallace", email="wWallace@freedom.com", password="password", role="final"),
    u3 = User.get_or_create(firstName="Tronchatoro", lastName="Teacher", email="tToroTeacher@email.com", password="password", role="admin")
    print([u1, u2, u3])
app.cli()