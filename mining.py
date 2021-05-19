import server
import threading
import time

shares_of_current_block = 0

miners = {}         # "account": number_of_shares
shares = {}         # dict of pplns_shares objects, every account has an element + pool has one
#TODO miner object for every miner/account, collect every miner related function to that

#TODO future feature: collect shares worker-by-worker for detailed stat
hr_shares = {}       # shares log for hashrate calculation for each account; example = {"1111":{"1":[timestamp1, timestamp2, timestamp3, ...], "32":[timestamp1, timestamp2, timestamp3, ..]}}
hr_avrg_shares = 30     # number of shares to calculated average hashrate

share_timeout = 240     # shares older than this will be deleted

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

def add_share_for_hr_calc(account, difficulty):
    global hr_shares

    account = str(account)
    difficulty = str(difficulty)

    diffs = []
    for diff in server.get_server_diffs():
        diffs.append(str(diff))

    if account in hr_shares:
        for diff in diffs:
            if len(hr_shares[account][diff]) == hr_avrg_shares:
                del hr_shares[account][diff][0]
    else:
        hr_shares[account] = {}
        for diff in diffs:
            hr_shares[account][diff] = []

    hr_shares[account][difficulty].append(time.time())

def get_hr(account):
    """
    Get hashrate for an account.
    Hashrate formula:
        hashrate = difficulty * 2**32 / avrg_share_time
    :param account:
    :return:
    """

    global hr_shares

    account = str(account)      # using account as str

    if account not in hr_shares:
        return 0

    diffs = []
    for diff in server.get_server_diffs():      # using diffs as str
        diffs.append(str(diff))

    hrs = []    # hashrate for every difficulty, then sum them for account hashrate

    for diff in diffs:
        if len(hr_shares[account][diff]) < 2:   # can't calculate from 0 or 1 shares
            continue

        # delete old shares
        new_timestamps = []
        for i in range(len(hr_shares[account][diff])):
            ts = hr_shares[account][diff][i]
            if (time.time() - ts) <= share_timeout:
                new_timestamps.append(ts)
        hr_shares[account][diff] = new_timestamps

        if len(hr_shares[account][diff]) < 2:   # can't calculate from 0 or 1 shares
            continue

        # get average share time
        last_share = hr_shares[account][diff][-1]
        first_share = hr_shares[account][diff][0]
        avrg_time = (last_share - first_share) / (len(hr_shares[account][diff]) - 1)
        new_hr = float(diff) * 2**32 / avrg_time
        hrs.append(new_hr)

    sum_hr = 0
    for hr in hrs:
        sum_hr += hr
    return sum_hr

def get_pool_hr():
    global hr_shares

    pool_hr = 0
    for account in hr_shares:
        pool_hr += get_hr(account)

    return pool_hr

def No_miners():
    return len(miner_conns)
