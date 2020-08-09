#!flask/bin/python
from flask import Flask, jsonify
import threading
from params import *
import mining

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route('/pool_data', methods=['GET'])
def get_pool_data():
    pool_data = {
        "algorithm": "Pascal",
        "poolhash": str(round(mining.get_pool_hr() / 10**9, 2)) + " Gh",
        "nethash":  0,
        "workers":  str(mining.No_miners()),
        "fee":      str(pool_fee) + "%",
        "period":   "Every block"
    }
    return jsonify({'pool_data': pool_data})

@app.route('/miner_data/<int:account>', methods=['GET'])
def get_miner_data(account):
    miner_data = {
        "account": str(account),
        "hashrate": str(round(mining.get_hr(account) / 10**9, 3)) + " Gh",
        "1hour":            0,
        "24hours":          0,
        "average_mined":    0
    }
    return jsonify({'miner_data': miner_data})

def start_restapi():
    app.run(debug=False, port = 3000)