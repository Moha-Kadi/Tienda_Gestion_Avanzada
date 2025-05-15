#   LIBRERÍAS
import datetime
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from decouple import config
URL_MONGO = config("ENLACE_DB", cast=str)

app = Flask(__name__)

#   CONEXIÓN MONGODB
mongo = MongoClient(URL_MONGO)
app.db = mongo.PythonMongoDB  

#   TABLAS MONGODB
Productos = [producto for producto in app.db.Productos.find({})]
Usuarios = [usuario for usuario in app.db.Usuarios.find({})]
Pedidos = [usuario for usuario in app.db.Pedidos.find({})]

#   DATOS
#   INFORMACIÓN GENERAL
info_general = {
    "admin": "moha",
    "tienda": "TecnoMarket",
    "fecha": datetime.date.today()
}

#   ENDPOINT
@app.route("/")
def home():
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
#   NÚMERO TOTAL DE PRODUCTOS EN STOCK
    total_stock = 0
    for total in Productos:
        total_stock += total["stock"]

    #   NÚMERO DE CLIENTES ACTIVOS
    clientes_activos = 0
    for cliente in Usuarios:
        if cliente["activo"]:
            clientes_activos += 1
    #   CLIENTE CON MAYOR NÚMERO DE PEDIDOS REALIZADOS
    nombre_cliente = ""
    max_pedidos = 0
    for cliente in Usuarios:
        if cliente["pedidos"] > max_pedidos:
            max_pedidos = cliente["pedidos"]
            nombre_cliente = cliente["nombre"]

    #   INGRESO TOTAL
    total_ingreso = 0
    for pedido in Pedidos:
        total_ingreso += pedido["total"]

    return render_template("dashboard.html", **info_general, products=Productos, total = total_stock , clientes=Usuarios, activos = clientes_activos, cliente_max_pedidos = nombre_cliente, pedidos=Pedidos, ingreso_total = total_ingreso)


@app.route("/añadir_producto", methods = ["GET", "POST"])
def añadir_producto():

    if request.method == "POST":
        
        nombre = request.form["nombre"]
        precio = f'{float(request.form["precio"]):.2f}'
        stock = int(request.form["stock"])
        categoria = request.form["categoria"]
        imagen = request.form["imagen"]

        parametros = {
            "nombre":nombre,
            "precio":precio,
            "stock":stock,
            "categoria":categoria,
            "img":imagen
            }
        
        Productos.append(parametros)
        app.db.Productos.insert_one(parametros)

        return redirect("/dashboard")

    return render_template("nuevo_producto.html")

@app.route("/productos")
def lista_productos():

    #   NÚMERO TOTAL DE PRODUCTOS EN STOCK
    total_stock = 0
    for total in Productos:
        total_stock += total["stock"]

    return render_template("lista_productos.html",products=Productos, total = total_stock)

@app.route("/productos/<id>")
def ver_producto(id):
    
    for producto in Productos:
        if producto["_id"] == id:
            return render_template("detalle_producto.html", productos=Productos)

    return render_template("404.html")
    

@app.route("/registro_usuario", methods = ["GET", "POST"])
def registro_usuario():

    if request.method == "POST":
        
        nombre = request.form["nombre"]
        email = request.form["email"]
        pedidos = int(request.form["pedidos"])
        imagen = request.form["imagen"]

        parametros = {
            "nombre":nombre,
            "email":email,
            "activo":True,
            "pedidos":pedidos,
            "img":imagen
            }
        
        Usuarios.append(parametros)
        app.db.Usuarios.insert_one(parametros)     

        return redirect("/dashboard")

    return render_template("registro_usuario.html")

@app.route("/usuarios")
def lista_usuarios():

    #   NÚMERO DE CLIENTES ACTIVOS
    clientes_activos = 0
    for cliente in Usuarios:
        if cliente["activo"]:
            clientes_activos += 1
    #   CLIENTE CON MAYOR NÚMERO DE PEDIDOS REALIZADOS
    nombre_cliente = ""
    max_pedidos = 0
    for cliente in Usuarios:
        if cliente["pedidos"] > max_pedidos:
            max_pedidos = cliente["pedidos"]
            nombre_cliente = cliente["nombre"]

    return render_template("lista_usuarios.html", clientes = Usuarios, activos = clientes_activos, cliente_max_pedidos = nombre_cliente)

if __name__ == "__main__":
    app.run(debug=True)