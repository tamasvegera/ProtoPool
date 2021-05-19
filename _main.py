import client
import server
import accountancy
import mining
import wallet_json_rpc
import restapi
import threading
import time
from params import *
from log_module import logger

#TODO
# - when miner connected before first mining-notify comes from wallet, it throws an error from stratum-47
# - rounding errors in balance calculation, example: from_account=1084190
# - wallet connection crashes sometimes after mining-submit
# - soft exit
#
class WalletNotFoundError(Exception):
    pass

def wallet_notify_watchdog():
    if client.last_miner_notify_flag is False:
        try:
            client.cli.close()
        except Exception as e:
            logger.error("WALLET notify watchdog error: " + str(e))
            pass
    client.last_miner_notify_flag = False
    threading.Timer(client.last_miner_notify_timeout, wallet_notify_watchdog, []).start()

print("Starting MicroCoin mining pool by vegtamas. Pool version: " + str(version))
logger.info("Starting MicroCoin mining pool by vegtamas. Pool version: " + str(version))

while True:
    print("Waiting for wallet sync")
    result = wallet_json_rpc.wait_for_wallet_start()
    if result is True:
        break
    time.sleep(5)

wallet_notify_watchdog()
wallet_json_rpc.get_public_key()

thread_client = threading.Thread(target=client.client_handler)
thread_client.start()

server.start_diff_servers()

#thread_mining_notify = threading.Thread(target=server.send_mining_notify_to_all)
#thread_mining_notify.start()

accountancy.start_payment_processor()
mining.print_stat()

restapi.start_restapi()
