import stratum
import threading

shares_of_current_block = 0

miners = {}         # "account": number_of_shares
shares = {}         # dict of pplns_shares objects, every account has an element + pool has one

class miner_conn():
    def __init__(self, connection, address):
        self.conn = connection
        self.addr = address
    def set_account(self, account):
        self.account = account
miner_conns = []

class pplns_shares():
    def __init__(self):
        self.timestamps = {}
    def add_share(self, timestamp, difficulty):
        self.timestamps[timestamp] = difficulty

def print_stat():
    global shares_of_current_block, miner_conns
    print("Number of connected miners: " + str(len(miner_conns)) + "  Running threads: " + str(threading.active_count()))
    threading.Timer(60, print_stat).start()