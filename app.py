import os
from flask import Flask
from wiki import fetch_entity

app = Flask(__name__)

@app.route("/age/<string:person>")
def hello(person):
    return fetch_entity(person)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port, host='0.0.0.0')
