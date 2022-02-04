#!flask/bin/python
from flask import Flask, jsonify, request

from params import pool_fee
import wallet_json_rpc
import mining
import sqlite_handler

app = Flask(__name__)

last_account_transferred_block = 0


class BePatientError(Exception):
    pass


def transfer_account_handler(new_pubkey):
    """
    It will transfer a random empty account to the new_pubkey. One account per block is allowed.
    :param new_pubkey:
    :return:
    """
    global last_account_transferred_block

    try:
        current_block = wallet_json_rpc.get_current_block()
    except wallet_json_rpc.WalletCommError:
        raise wallet_json_rpc.WalletCommError

    if current_block == last_account_transferred_block:
        raise BePatientError

    try:
        acc_number = wallet_json_rpc.get_a_zero_balance_account_number()
    except wallet_json_rpc.WalletCommError:
        raise wallet_json_rpc.WalletCommError
    except wallet_json_rpc.NoEmptyAccountError:
        raise wallet_json_rpc.NoEmptyAccountError

    try:
        wallet_json_rpc.change_key(new_pubkey, acc_number)
    except wallet_json_rpc.WalletCommError:
        raise wallet_json_rpc.WalletCommError
    except wallet_json_rpc.InputParameterError:
        raise wallet_json_rpc.InputParameterError

    last_account_transferred_block = current_block
    return True

@app.route('/pool_data', methods=['GET'])
def get_pool_data():
    network_height = wallet_json_rpc.get_current_block()
    pool_data = {
        "current_block": str(network_height),
        "net_hashrate": str(wallet_json_rpc.get_net_hashrate(network_height)) + " Gh",
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
        "average_mined":    0,
        "payments":         sqlite_handler.db.get_account_payments(account)
    }
    return jsonify({'miner_data': miner_data})

@app.route('/get_account', methods=['POST'])
def get_account():
    pubkey = request.form['pubkey']
    try:
        transfer_account_handler(pubkey)
    except wallet_json_rpc.WalletCommError:
        return jsonify({'result': 'An error occured on the pool side. Please try again. If you see this message multiple times please report it to the team on Discord or Telegram. Thank you!'})
    except BePatientError:
        return jsonify({'result': 'An account was already sent to someone in this block. Please try again in a few minutes. If you see this message multiple times please report it to the team on Discord or Telegram. Thank you!'})
    except wallet_json_rpc.NoEmptyAccountError:
        return jsonify({'result': 'No free account is left on the pool. Please try again in a few minutes. If you see this message multiple times please report it to the team on Discord or Telegram. Thank you!'})
    except wallet_json_rpc.InputParameterError:
        return jsonify({'result': 'Wrong public key! You can export your public key from the wallet. It has to start with "3G". If you see this message multiple times please report it to the team on Discord or Telegram. Thank you!'})

    return jsonify({'result': 'An empty account was successfully sent to your public key. You will see it in the next block in appr. 5 minutes.'})

def start_restapi():
    app.run(debug=False, port = 3000)
