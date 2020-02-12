import client, server, accountancy, mining, wallet_json_rpc
import threading, os, subprocess, requests, json, time, psutil, sys, log_module
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

def is_wallet_running():
    if "MicroCoinWallet.exe" in (p.name() for p in psutil.process_iter()):
        return True
    else:
        return False

def start_wallet():
    if is_wallet_running() == False:
        try:
            subprocess.Popen(wallet_path + " &")
        except FileNotFoundError:
            raise WalletNotFoundError

def kill_wallet():
    if is_wallet_running():
        os.system("taskkill /f /im MicroCoinWallet.exe")

def wallet_watchdog():
    if wallet_json_rpc.wallet_has_nodes() == False:
        logger.info("WALLET restarted")
        kill_wallet()
        time.sleep(10)
        print("Wallet is restarted.")
        start_wallet()
    threading.Timer(5, wallet_watchdog, []).start()

def wallet_notify_watchdog():
    if client.last_miner_notify_flag == False:
        try:
            client.cli.close()
        except Exception as e:
            logger.error("WALLET notify watchdog error: " + str(e))
            pass
    client.last_miner_notify_flag = False
    threading.Timer(client.last_miner_notify_timeout, wallet_notify_watchdog, []).start()

try:
    start_wallet()
except WalletNotFoundError:
    print("Wallet not found at the given path. Check wallet path")
    print("Program will be terminated in 5 seconds.")
    time.sleep(5)
    sys.exit()

print("Waiting wallet to start")
while True:
    result = wallet_json_rpc.wait_for_wallet_start()
    if result == True:
        break

wallet_watchdog()
wallet_notify_watchdog()
wallet_json_rpc.get_public_key()
thread_client = threading.Thread(target=client.client_handler)
thread_client.start()

server.start_diff_servers()

#thread_mining_notify = threading.Thread(target=server.send_mining_notify_to_all)
#thread_mining_notify.start()

# TODO uncomment line below!
accountancy.payment_processor()
mining.print_stat()
