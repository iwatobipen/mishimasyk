from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template
def create_app():
    app = Flask( __name__ )
    Bootstrap( app )

    return app

app = create_app()
@app.route("/")
def root():
    return render_template("top.html")
@app.route("/circle")
def circle():
    return render_template("circle.html")
@app.route("/cola")
def cola():
    return render_template("cola.html")
@app.route("/concentric")
def concentric():
    return render_template("concentric.html")
@app.route("/cose")
def cose():
    return render_template("cose.html")
@app.route("/grid")
def grid():
    return render_template("grid.html")
@app.route("/dagre")
def dagre():
    return render_template("dagre.html")
@app.route("/arbor")
def arbor():
    return render_template("arbor.html")




if __name__=="__main__":
    app.run(debug = True)

