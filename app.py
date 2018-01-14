import sys
from flask import Flask
from wiki import fetch_entity

app = Flask(__name__)

@app.route("/age/<string:person>")
def hello(person):
    return fetch_entity(person)

if __name__ == '__main__':
    port = int(sys.argv[1])
    app.run(port=port)
