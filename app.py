import os
from flask import Flask, Response, redirect, url_for, request, render_template
from pymongo import MongoClient
from middleware import setup_metrics
import prometheus_client

app = Flask(__name__)

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

client = MongoClient(
    'db',
    27017)
db = client.tododb

setup_metrics(app)

@app.route('/')
def todo():

    _items = db.tododb.find()
    items = [item for item in _items]

    return render_template('todo.html', items=items)


@app.route('/new', methods=['POST'])
def new():

    item_doc = {
        'name': request.form['name'],
        'description': request.form['description']
    }
    db.tododb.insert_one(item_doc)

    return redirect(url_for('todo'))

@app.route('/metrics', methods=['GET'])
def metrics():
    return Response(prometheus_client.generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run( host='0.0.0.0' )
