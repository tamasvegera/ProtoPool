import socket, threading, ast, json
import server, accountancy, wallet_json_rpc, mysql_handler

last_miner_notify_flag = True
last_miner_notify = ["", "", ""]
last_miner_notify_cnt = 0
last_miner_notify_buf_full = False

last_miner_notify_timeout = 180

host = 'localhost'
port = 4009
buffer = 4096

cli = None


def client_handler():
    global last_miner_notify, cli, last_miner_notify_cnt, last_miner_notify_buf_full, last_miner_notify_flag
    wallet_ok = False
    while True:

        print("Client to wallet is starting...")
        try:
            cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cli.connect((host, port))
            wallet_ok = True
            print("Client to wallet started")
        except:
            print("Client to wallet cannot be started.")
            wallet_ok = False

        while wallet_ok == True:
            try:
                data = cli.recv(buffer)
            except:
                wallet_ok = False
                cli.close()
                break
            if not data:
                cli.close()
                break
            data_str = data.decode("utf-8")
            print("From wallet:" + data_str)
            data_str = data_str.replace('null', '"null"')
            msgs = data_str.split('\n')
            for msg in msgs:
                try:
                    msg = json.loads(msg)
                except:
                    continue
                if "method" in msg:
                    if msg["method"] == "miner-notify":
                        last_miner_notify_cnt += 1
                        if last_miner_notify_cnt == 2:
                            last_miner_notify_buf_full = True
                            last_miner_notify_cnt = 0
                        last_miner_notify[last_miner_notify_cnt] = msg
                        accountancy.current_block = msg["params"][0]["block"]
                        server.send_mining_notify_to_all()
                        last_miner_notify_flag = True

                if "result" in msg:
                    if "pow" in msg["result"]:
                        print(
                            "NEW BLOCK FOUND!! YEEEE  NEW BLOCK FOUND!! YEEEE  NEW BLOCK FOUND!! YEEEE  NEW BLOCK FOUND!! YEEEE  NEW BLOCK FOUND!! YEEEE")
                        #mysql_handler.set_block_to_acked_by_wallet(msg["result"]["block"])
                        #new block accountancy moved
                        #accountancy.new_block_accountancy()


def mining_submit_handler(submit_msg, extranonce):
    global last_miner_notify, last_miner_notify_cnt
    timestamp_dec = str(int(submit_msg["params"][3], 16))
    nonce = str(int(submit_msg["params"][4], 16))
    payload = extranonce + submit_msg["params"][2]
    msg = '{"id": 10, "method": "miner-submit", "params": [{"payload": "' + payload + '","timestamp":' + timestamp_dec + ',"nonce":' + nonce + '}]}\n'
    print("To wallet: " + msg)

    print("Wallet ok:   " + str(wallet_json_rpc.wallet_ok))

    if wallet_json_rpc.wallet_ok == True:
        cli.sendall(msg.encode())
        #DELETE THE LINE BELOW
        #wallet_json_rpc.wallet_ok = False