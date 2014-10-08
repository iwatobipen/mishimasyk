from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template
def create_app():
    app = Flask( __name__ )
    Bootstrap( app )

    return app

app = create_app()

@app.route("/")
def example():
    return render_template("hoge.html")


if __name__=="__main__":
    app.run(debug = True)

