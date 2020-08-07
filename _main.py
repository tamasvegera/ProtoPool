import client, server, accountancy, mining, wallet_json_rpc
import threading, time
from params import *
from log_module import *

#TODO
# - when miner connected before first mining-notify comes from wallet, it throws an error from stratum-47
# - rounding errors in balance calculation, example: from_account=1084190
# - wallet connection crashes sometimes after mining-submit
#
#
class WalletNotFoundError(Exception):
    pass

def wallet_notify_watchdog():
    if client.last_miner_notify_flag == False:
        try:
            client.cli.close()
        except Exception as e:
            logger.error("WALLET notify watchdog error: " + str(e))
            pass
    client.last_miner_notify_flag = False
    threading.Timer(client.last_miner_notify_timeout, wallet_notify_watchdog, []).start()

print("Starting MicroCoin mining pool by vegtamas. Pool version: " + str(version))
while True:
    print("Waiting for wallet sync")
    result = wallet_json_rpc.wait_for_wallet_start()
    if result == True:
        break
    time.sleep(5)

wallet_notify_watchdog()
if wallet_json_rpc.get_public_key() == "nokey":
    wallet_json_rpc.add_main_pub_key()

thread_client = threading.Thread(target=client.client_handler)
thread_client.start()

server.start_diff_servers()

#thread_mining_notify = threading.Thread(target=server.send_mining_notify_to_all)
#thread_mining_notify.start()

# TODO uncomment line below!
accountancy.payment_processor()
mining.print_stat()
