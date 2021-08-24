from flask import *
from flaskext.mysql import MySQL
import pymysql

app=Flask(__name__)


db=pymysql.connect(host='localhost',user='root', password='',db='CARIPE')

MySQL(app)


app.secret_key='somesecretkeythantonlyishouldknow'

@app.before_request
def before_request():
    g.user=None
    if "user_id" in session:
        user = [x for x in users if x.id==session["user_id"]][0]
        g.user = user







@app.route('/agregar-reservacion', methods=['POST'])
def agregar_reservacion():
    if request.method == 'POST':
        paquete=request.form['paquete']
        ingreso=request.form['ingreso']
        salida=request.form['salida']
        nombre=request.form['nombre']
        telefono=request.form['telefono']
        email=request.form['email']
        mensaje=request.form['mensaje']

        if paquete=="" or ingreso=="" or salida=="" or nombre=="" or telefono=="" or email=="":
           return redirect(url_for('home'))
           

        cursor = db.cursor()
        cursor.execute('INSERT INTO RESERVACIONES (PAQUETE, INGRESO, SALIDA, NOMBRE, TELEFONO, CORREO, MENSAJE) VALUES (%s, %s, %s,%s, %s, %s, %s)', (paquete,ingreso, salida, nombre, telefono, email, mensaje))
        cursor.connection.commit()
        # flash('Contacto Agregado con exito')
        return redirect(url_for('home'))





@app.route('/')
def home():
    micursor=db.cursor()
    micursor.execute("SELECT * FROM PAQUETES")
    datos1=micursor.fetchall()
    micursor.connection.commit()
    return render_template('home.html' , seccion='inicio', paquetes=datos1)




@app.route('/reservacion')
def reservacion():

    return render_template('reservacion.html', seccion='reservacion')

@app.route('/paquetes')
def paquetes():
    micursor=db.cursor()
    micursor.execute("SELECT * FROM PAQUETES")
    datos1=micursor.fetchall()
    micursor.connection.commit()
    return render_template('paquete.html', seccion='paquetes', paquetes=datos1)



# Administracion
class User:
    def __init__(self,id,username,password):
        self.id=id;
        self.username=username;
        self.password=password;

    def __repr__(self):
        return f'<User: {self.username}';




users=[];

micursor=db.cursor()
micursor.execute("SELECT * FROM ADMINISTRADORES")
datos=micursor.fetchall()
for i in datos:
    users.append(User(id=i[0],username=i[2],password=i[3]))

micursor.connection.commit()

print(users)

@app.route('/login',methods=["GET", "POST"])
def login():
    
    acceso=True
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']

        micursor=db.cursor()
        micursor.execute("SELECT * FROM ADMINISTRADORES WHERE USUARIO=%s AND CONTRASEÑA=%s",(username, password))
        datos=micursor.fetchall()
        
        micursor.connection.commit()
        if datos==():
            acceso=False
            session.pop("user_id",None)

            return render_template("login.html",acceso="no")

        session.pop("user_id",None)

        user=[x for x in users if x.username==username][0]
        if user and user.password==password:
            session["user_id"]=user.id
            return redirect(url_for("inicio"))

        return redirect(url_for("login"))
    g.user=None
    session.pop("user_id",None)
   
    return render_template("login.html")



    
@app.route('/inicio')
def inicio ():
    
    micursor=db.cursor()
    micursor.execute("SELECT * FROM RESERVACIONES")
    datos=micursor.fetchall()
    micursor.connection.commit()
    if not g.user:
        return redirect(url_for("login"))
    return render_template('administracion/index.html',datos=datos,seccion='inicio')




@app.route('/reservacion/<id>')
def ver_reservacion(id):
    if not g.user:
        return redirect(url_for("login"))


    micursor=db.cursor()
    micursor.execute("SELECT * FROM RESERVACIONES WHERE id=%s",(id, ))
    datos=micursor.fetchall()
    micursor.connection.commit()


    return render_template('administracion/ver_reservacion.html',datos=datos,seccion='inicio')

@app.route("/editar-paquetes")
def editar_paquetes():
    if not g.user:
        return redirect(url_for("login"))

    micursor=db.cursor()
    micursor.execute("SELECT * FROM PAQUETES WHERE PAQUETE='Paquete 1'")
    datos1=micursor.fetchall()
    micursor.execute("SELECT * FROM PAQUETES WHERE PAQUETE='Paquete 2'")
    datos2=micursor.fetchall()
    micursor.execute("SELECT * FROM PAQUETES WHERE PAQUETE='Paquete 3'")
    datos3=micursor.fetchall()
    micursor.connection.commit()

    return render_template("administracion/paquetes.html",seccion="paquetes",paquetes=[datos1,datos2,datos3])


@app.route("/actualizar-paquetes",methods=["POST"])
def actualizar_paquetes():
    if not g.user:
        return redirect(url_for("login"))

    if request.method=="POST":
        precio_1=request.form['precio-1']
        servicio_1_1=request.form['servicio-1-1']
        servicio_2_1=request.form['servicio-2-1']
        servicio_3_1=request.form['servicio-3-1']
        mensaje_1=request.form['mensaje-1']
        
        precio_2=request.form['precio-2']
        servicio_1_2=request.form['servicio-1-2']
        servicio_2_2=request.form['servicio-2-2']
        servicio_3_2=request.form['servicio-3-2']
        mensaje_2=request.form['mensaje-2']

        precio_3=request.form['precio-3']
        servicio_1_3=request.form['servicio-1-3']
        servicio_2_3=request.form['servicio-2-3']
        servicio_3_3=request.form['servicio-3-3']
        mensaje_3=request.form['mensaje-3']

        micursor=db.cursor()
        micursor.execute("UPDATE PAQUETES SET PRECIO=%s,SERVICIO1=%s,SERVICIO2=%s,SERVICIO3=%s,MENSAJE=%s WHERE PAQUETE='Paquete 1'",(precio_1,servicio_1_1,servicio_2_1,servicio_3_1,mensaje_1))
        micursor.execute("UPDATE PAQUETES SET PRECIO=%s,SERVICIO1=%s,SERVICIO2=%s,SERVICIO3=%s,MENSAJE=%s WHERE PAQUETE='Paquete 2'",(precio_2,servicio_1_2,servicio_2_2,servicio_3_2,mensaje_2))
        micursor.execute("UPDATE PAQUETES SET PRECIO=%s,SERVICIO1=%s,SERVICIO2=%s,SERVICIO3=%s,MENSAJE=%s WHERE PAQUETE='Paquete 3'",(precio_3,servicio_1_3,servicio_2_3,servicio_3_3,mensaje_3))
        datos=micursor.fetchall()
        micursor.connection.commit()

        return redirect(url_for("editar_paquetes"))




@app.route('/borrar-reservacion/<id>')
def borrar_reservacion(id):

    micursor=db.cursor()
    micursor.execute("DELETE FROM RESERVACIONES WHERE id=%s",(id))
    datos=micursor.fetchall()
    micursor.connection.commit()
    return redirect(url_for('inicio'))



if __name__=='__main__':

	app.run(port=5000,debug=True)
