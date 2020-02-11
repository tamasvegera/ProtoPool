import requests, json, accountancy
from params import *

maturation_time = 10        # in blocks
wallet_password = "your_password"
wallet_name = "protopool"
wallet_server_ip = 'http://localhost'
wallet_server_port = 4003
wallet_server_ip_port = wallet_server_ip + ':' + str(wallet_server_port)

pool_public_key = 0

wallet_ok = False

class WalletPubKeyError(Exception):
    pass

class WalletInvalidOperationError(Exception):
    pass

class WalletNotReadyError(Exception):
    pass

def get_block_reward(block):
    msg = {"jsonrpc": "2.0", "method": "getblock", "params": {"block": block}, "id": 123}
    response_raw = requests.post(wallet_server_ip_port, json=msg)
    response = json.loads(response_raw.text)
    if "result" not in response:
        print("From wallet jsonrpc: " + str(response))
        return False

    return response["result"]["reward"] + response["result"]["fee"]

def is_block_matured(block):
    msg = {"jsonrpc": "2.0", "method": "getblock", "params": {"block": block}, "id": 123}
    response_raw = requests.post(wallet_server_ip_port, json=msg)
    response = json.loads(response_raw.text)

    if "result" not in response:
        print("From wallet jsonrpc: " + str(response))
        return False

    if response["result"]["maturation"] >= maturation_time:
        return True
    else:
        return False

def check_block_pubkey(block):
    msg = {"jsonrpc": "2.0", "method": "getblock", "params": {"block": block}, "id": 123}
    response_raw = requests.post(wallet_server_ip_port, json=msg)
    response = json.loads(response_raw.text)

    if "result" not in response:
        print("From wallet jsonrpc: " + str(response))
        return False
    enc_pubkey = response["result"]["enc_pubkey"]

    if enc_pubkey == pool_public_key:
        return True
    else:
        return False

def get_last_block():
    msg = {"jsonrpc": "2.0", "method": "getblockcount", "params": {"last": 1}, "id": 123}
    response_raw = requests.post(wallet_server_ip_port, json=msg)
    response = json.loads(response_raw.text)
    last_block = response["result"]
    return last_block

def get_last_account():
    data = {"jsonrpc": "2.0", "method": "getwalletaccountscount", "id": 123}
    response_raw = requests.post(wallet_server_ip_port, json=data)
    response = json.loads(response_raw.text)

    msg = {"jsonrpc":"2.0","method":"getwalletaccounts","params":{"start":response["result"]-5},"id":123}
    response_raw = requests.post(wallet_server_ip_port, json=msg)
    response = json.loads(response_raw.text)
    wallet = {"account": response["result"][0]["account"], "balance":response["result"][0]["balance"]}
    return wallet

def unlock_wallet():
    msg = {"jsonrpc": "2.0", "method": "unlock", "params": {"pwd": wallet_password}, "id": 123}
    response_raw = requests.post(wallet_server_ip_port, json=msg)
    response = json.loads(response_raw.text)
    if response["result"] == True:
        print("Wallet unlocked")
    else:
        print("Wallet can't be unlocked.")

def lock_wallet():
    msg = {"jsonrpc": "2.0", "method": "lock", "id": 123}
    response_raw = requests.post(wallet_server_ip_port, json=msg)
    response = json.loads(response_raw.text)

def send_payment(from_account, to_account, amount, block):
    if wallet_ok == False:
        raise WalletNotReadyError

#TODO uncomment payload
    payload = ""#""pool share, block: " + str(block)
    payload = payload.encode('utf-8')
    msg = {"jsonrpc":"2.0","method":"sendto","params":{"sender":from_account,"target":to_account,"amount":amount,"fee":accountancy.payment_fee,"payload":payload.hex(),"payload_method":"none","pwd":wallet_password},"id":123}
    response_raw = requests.post(wallet_server_ip_port, json=msg)
    response = json.loads(response_raw.text)

    if "result" in response:
        print("Payment sent from: " + str(from_account) + " to: " + str(to_account) + ", amount: " + str(amount))
    else:
        #print("Payment ERROR from: " + str(from_account) + " to: " + str(to_account) + ", amount: " + str(amount) + "  " + response["error"]["message"])
        if response["error"]["code"] == 1004:
            raise WalletInvalidOperationError
        elif response["error"]["code"] == 1005:       # invalid public key -> orphan
            raise WalletPubKeyError
        else:
            raise Exception

def wallet_has_nodes():
    global wallet_ok
    try:
        data = {"jsonrpc": "2.0", "method": "nodestatus", "params": {}, "id": 123}
        response_raw = requests.post(wallet_server_ip_port, json=data)
        response = json.loads(response_raw.text)
        if response["result"]["ready"] == False and response["result"]["ready_s"] == "Alone in the world...":
            wallet_ok = False
            return False
        else:
            wallet_ok = True
            return True
    except:
        wallet_ok = False
        return False

def wait_for_wallet_start():
    global wallet_ok
    try:
        while True:
            data = {"jsonrpc": "2.0", "method": "nodestatus", "params": {}, "id": 123}
            response_raw = requests.post(wallet_server_ip_port, json=data)
            response = json.loads(response_raw.text)
            if "status_s" in response["result"]:
                if response["result"]["status_s"] == "Running":
                    return True
            return False
    except:
        wallet_ok = False
        return False

def get_public_key():
    global pool_public_key
    try:
        data = {"jsonrpc": "2.0", "method": "getwalletpubkeys", "id": 123}
        response_raw = requests.post(wallet_server_ip_port, json=data)
        response = json.loads(response_raw.text)
        for key in response["result"]:
            if key["name"] == wallet_name:
                pool_public_key = key["enc_pubkey"]
    except:
        wallet_ok = False
        return False

def get_account_balance(account):
    data = {"jsonrpc": "2.0", "method": "getaccount", "params":{"account":account}, "id": 123}
    response_raw = requests.post(wallet_server_ip_port, json=data)
    response = json.loads(response_raw.text)
    return response["result"]["balance"]