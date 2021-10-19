from flask import Flask
from flask import render_template as render
from flask import redirect
from flask import request
app = Flask(__name__)

@app.route("/")
def inicio():
    return render("index.html")

@app.route("/edit_product/<product_id>", methods=["GET", "POST"])
def editProduct(product_id):
    if request.method == "GET" :
        return render('edit_product.html')
    else:
        return redirect("/inicio")

@app.route("/delete_product/<product_id>", methods=["GET", "POST"])
def deleteProduct(product_id):
    return f"delete the product {product_id}"

@app.route("/califications/<product_id>", methods=["GET", "POST"])
def getCalifications(product_id):
    return render("califications.html")

if __name__ == "__main__":
        app.run(debug=True)
