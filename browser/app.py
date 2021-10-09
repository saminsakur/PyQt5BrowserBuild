from flask import Flask, render_template
import sys

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

app = Flask(__name__)

@app.route("/")
def server():
    return render_template("index.html")

# app.run(debug=True)
