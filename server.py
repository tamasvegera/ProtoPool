import threading
import socket
import time
import ast
import binascii
import hashlib

import client
import mining
import stratum
import accountancy

host = ''
diffs = [1,32]
diff_ports = [3333,3334]
max_conn = 200

def get_server_diffs():
    return diffs

def send_mining_notify_to_all():
    for miner in mining.miner_conns[:]:
        thread = threading.Thread(target=stratum.send_mining_notify,args=(miner, 'null'))
        thread.start()

def calc_block_pow(part1, payload, part3, timestamp, nonce):
       part1_raw = binascii.unhexlify(part1)
       payload_raw = binascii.unhexlify(payload)
       part3_raw = binascii.unhexlify(part3)

       new_timestamp = timestamp[6:] + timestamp[4:6] + timestamp[2:4] + timestamp[0:2]
       new_timestamp_raw = binascii.unhexlify(new_timestamp)
       new_nonce= nonce[6:] + nonce[4:6] + nonce[2:4] + nonce[0:2]
       new_nonce_raw = binascii.unhexlify(new_nonce)
       to_hash = part1_raw + payload_raw + part3_raw + new_timestamp_raw + new_nonce_raw
       d = hashlib.sha256(to_hash)
       d2 = hashlib.sha256()
       d2.update(d.digest())
       return int(d2.hexdigest(),16)

def get_block_pow(payload, timestamp, nonce):
    pow1 = calc_block_pow(client.last_miner_notify[1]["params"][0]["part1"], payload, client.last_miner_notify[1]["params"][0]["part3"], timestamp, nonce)
    if client.last_miner_notify_buf_full:
        pow2 = calc_block_pow(client.last_miner_notify[0]["params"][0]["part1"], payload, client.last_miner_notify[0]["params"][0]["part3"], timestamp, nonce)
    else:
        return pow1

    if pow1 > pow2:
        return pow2
    else:
        return pow1

def calc_diff_from_target(target):
    maximum_target = 0x00000000FFFF0000000000000000000000000000000000000000000000000000
    difficulty = maximum_target / target
    return difficulty

def close_miner_conn(miner):
    if miner in mining.miner_conns:
        mining.miner_conns.remove(miner)
    miner.conn.close()

def connection_handler(conn, addr, difficulty):
    account = 0
    extranonce = 0
    new_miner = mining.miner_conn(conn, addr)
    last_payload = ''
    last_timestamp = ''
    last_nonce = ''

    while True:
        try:
            buf = new_miner.conn.recv(4096)
        except:
            print("Miner disconnected from " + new_miner.addr[0] + ':' + str(new_miner.addr[1]))
            try:
                close_miner_conn(new_miner)
            except:
                pass
            break
        if buf:
            try:
                msgs = buf.decode("utf-8")
                msgs = msgs.split('\n')
            except:
                close_miner_conn(new_miner)
                continue
            #print("From miner @" + new_miner.addr[0] + ': ' + msgs)
            for msg in msgs:
                if msg:
                    try:
                        msg = ast.literal_eval(msg)
                    except:
                        continue
                else:
                    continue
                if "method" not in msg:
                    continue
                if msg["method"] == "mining.subscribe":
                    extranonce = stratum.send_subscribe_ack(new_miner, msg["id"])
                    stratum.send_difficulty(new_miner, difficulty, msg["id"])
                    stratum.send_mining_notify(new_miner, msg[id])

                elif msg["method"] == "mining.authorize":
                    try:
                        #TODO check if account is a valid account number!
                        account = int(((msg["params"][0]).split('-'))[0])
                        try:
                            accountancy.account_fees[account] = int(msg["params"][1])
                        except:
                            accountancy.account_fees[account] = accountancy.pool_fee
                        if accountancy.account_fees[account] < accountancy.pool_fee or accountancy.account_fees[account] > 100:
                            accountancy.account_fees[account] = accountancy.pool_fee
                    except:
                        print("Wrong account name")
                        stratum.send_auth_error(new_miner, msg["id"])
                        new_miner.conn.close()
                        break   #TODO send error msg

                    new_miner.set_account(account)
                    mining.miner_conns.append(new_miner)
                    if account not in mining.miners:
                        mining.shares[account] = new_miner
                        mining.miners[account] = 0      #set shares to 0 for that account
                    stratum.send_auth_ack(new_miner,msg["id"])

                elif msg["method"] == "mining.submit":
                    payload = extranonce + msg["params"][2]
                    if last_payload == payload and last_timestamp == msg["params"][3] and last_nonce == msg["params"][4]:
                        stratum.send_submit_error(new_miner, msg["id"])
                        #print("Share rejected because of duplication from: " + new_miner.addr[0])
                    else:
                        block_pow = get_block_pow(payload, msg["params"][3], msg["params"][4])
                        target_pow = int(client.last_miner_notify[client.last_miner_notify_cnt]["params"][0]["target_pow"], 16)
                        #print(calc_diff_from_target(block_pow))
                        if calc_diff_from_target(block_pow) >= difficulty:
                            stratum.send_submit_ack(new_miner, msg["id"])
                            timestamp = time.time()
                            mining.shares[account].add_share(timestamp, difficulty)
                            mining.add_share_for_hr_calc(account, difficulty)
                            #print("Share accepted from: " + new_miner.addr[0])
                        else:
                            stratum.send_submit_error(new_miner, msg["id"])
                            #print("Share rejected from: " + new_miner.addr[0])
                        if block_pow <= target_pow:
                            print("Block found with this share from: " + new_miner.addr[0])
                            client.mining_submit_handler(msg, extranonce)
                    last_payload = payload
                    last_timestamp = msg["params"][3]
                    last_nonce = msg["params"][4]
                elif msg["method"] == "mining.extranonce.subscribe":
                    stratum.send_extranonce_subscribe_ack(new_miner, msg["id"])
        else:
            close_miner_conn(new_miner)

def server_handler(diff, diff_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host,diff_port))
    server.listen(max_conn)
    print("Server started, diff: " + str(diff) + ", port: " + str(diff_port))
    while True:
        conn, addr = server.accept()
        print("Miner connected from: " + addr[0] + ':' + str(addr[1]))
        thread = threading.Thread(target=connection_handler, args=(conn,addr,diff))
        thread.start()

def start_diff_servers():
    global diffs, diff_ports
    for i in range(len(diffs)):
        thread_server = threading.Thread(target=server_handler, args=(diffs[i],diff_ports[i]))
        thread_server.start()
