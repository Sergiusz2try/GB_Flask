from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello world!'


@app.route("/greet/<string:name>/")
def greet_name(name: str):
    return f"Hello {name}!"
