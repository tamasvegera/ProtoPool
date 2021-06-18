import client
import server
from log_module import logger

extranonce2_size = 8
job_id = 0

unique_miner_id_cnt = 1
needed_extranonce_size = 26

def send_tcp_msg(miner, msg):
    try:
        #print("Sending to " + addr[0] + ':' + str(addr[1]) + ': ' + msg)
        miner.conn.sendall(msg.encode())
    except Exception as e:
        logger.error("Sending failed to " + miner.addr[0] + ':' + str(miner.addr[1]) + "  error: " + str(e))
        print("Sending failed to " + miner.addr[0] + ':' + str(miner.addr[1]))
        server.close_miner_conn(miner)

def send_stratum_msg(miner, id, method, params):

    if id == 'null':
        msg = '{"id":null,'
    else:
        msg = '{"id":' + str(id) + ','

    msg = msg + '"method":"' + method + '",'
    msg = msg + '"params":['
    msg = msg + '"' + params[0] + '",'
    msg = msg + '"' + params[1] + '",'
    msg = msg + '"' + params[2] + '",'
    msg = msg + '"' + params[3] + '",'
    msg = msg + str(params[4]) + ','
    msg = msg + '"' + params[5] + '",'
    msg = msg + '"' + params[6] + '",'
    msg = msg + '"' + params[7] + '",'
    msg = msg + params[8]
    msg = msg + ']}\n'

    send_tcp_msg(miner,msg)

def send_subscribe_ack(miner, id):
    global extranonce2_size, unique_miner_id_cnt, needed_extranonce_size

    val_str = str(unique_miner_id_cnt)
    hex_text = ''
    for i in range(len(val_str)):
        char = val_str[i]
        hex_text = hex_text + str(hex(int(char) + 48)[2:])

    extranonce = client.last_miner_notify[client.last_miner_notify_cnt]["params"][0]["payload_start"] + hex_text

    add_zeros = needed_extranonce_size - int(len(extranonce)/2)
    for i in range(add_zeros):
        extranonce = extranonce + '30'

    unique_miner_id_cnt += 1
    msg = '{"id":' + str(id) + ', "error": null, "result": [[["mining.notify", "00000000000000000000000000000000"]],"' + extranonce + '",' + str(extranonce2_size) + ']}\n'
    send_tcp_msg(miner, msg)
    return extranonce

def send_difficulty(miner, difficulty, id):
    msg = '{"id":' + str(id) + ', "method": "mining.set_difficulty", "params": [' + str(difficulty) + ']}\n'
    send_tcp_msg(miner, msg)

def send_auth_ack(miner,id):
    msg = '{"id":' + str(id) + ', "result": true, "error": null}\n'
    send_tcp_msg(miner,msg)

def send_auth_error(miner, id):
    error = '{"id":' + str(id) + ', "result": null, "error": [20, "Wrong username!", null]}'
    msg = '{"id":' + str(id) + ', "result": null, "error":' + str(error) + '}\n'
    send_tcp_msg(miner, msg)

def send_submit_ack(miner,id):
    msg = '{"id":' + str(id) + ',"result":true,"error":null}\n'
    send_tcp_msg(miner,msg)

def send_submit_error(miner,id):
    msg = '{"id":' + str(id) + ',"result":false,"error":null}\n'
    send_tcp_msg(miner,msg)

def send_extranonce_subscribe_ack(miner, id):
    msg = '{"id":' + str(id) + ', "error": null, "result": true}\n'
    send_tcp_msg(miner,msg)

def send_mining_notify(miner, id):
    global job_id
    params = []
    params.append(str(hex(job_id)[2:]))
    params.append("0000000000000000000000000000000000000000000000000000000000000000")
    params.append(client.last_miner_notify[client.last_miner_notify_cnt]["params"][0]["part1"])
    params.append(client.last_miner_notify[client.last_miner_notify_cnt]["params"][0]["part3"])
    params.append([])
    params.append("00000000")
    params.append(str(hex(client.last_miner_notify[client.last_miner_notify_cnt]["params"][0]["target"])[2:]))
    params.append(str(hex(client.last_miner_notify[client.last_miner_notify_cnt]["params"][0]["timestamp"])[2:]))
    params.append('true')

    send_stratum_msg(miner, id, 'mining.notify', params)
    job_id += 1
    params[0] = str(hex(job_id)[2:])
    params[8] = 'true'
    #send_stratum_msg(miner, 'null', 'mining.notify', params)
    job_id += 1
