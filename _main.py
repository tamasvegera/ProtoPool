import client, server, accountancy, mining, wallet_json_rpc
import threading, os, subprocess, requests, json, time

def wallet_watchdog():
    if wallet_json_rpc.wallet_has_nodes() == False:
        try:
            os.system("taskkill /f /im MicroCoinWallet.exe")
            time.sleep(10)
        except:
            pass
        print("Wallet is restarted.")
        subprocess.Popen("C:\\Users\\Administrator\\Documents\\crypto\\MicroCoin\\MicroCoin\\MicroCoinWallet.exe &", shell=True)
        #subprocess.Popen("C:\\Users\\Administrator\\Documents\\crypto\\MicroCoin\\MicroCoin\\wallet_1.1.2\\MicroCoinWallet.exe &", shell=True)
    threading.Timer(5, wallet_watchdog, []).start()

def wallet_notify_watchdog():
    if client.last_miner_notify_flag == False:
        try:
            client.cli.close()
        except:
            pass
    client.last_miner_notify_flag = False
    threading.Timer(client.last_miner_notify_timeout, wallet_notify_watchdog, []).start()

wallet_watchdog()
print("Waiting wallet to start")
while True:
    result = wallet_json_rpc.wait_for_wallet_start()
    if result == True:
        break

wallet_notify_watchdog()
wallet_json_rpc.get_public_key()
thread_client = threading.Thread(target=client.client_handler)
thread_client.start()

server.start_diff_servers()

#thread_mining_notify = threading.Thread(target=server.send_mining_notify_to_all)
#thread_mining_notify.start()

accountancy.payment_processor()
mining.print_stat()
