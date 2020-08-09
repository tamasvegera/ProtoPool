import json
with open('config.txt') as f:
    config_data = json.load(f)

version = 2.0

# user config
payment_fee_to_pool = config_data["payment_fee_to_pool"]        # this fee will be sent to pool address in order to prevent tx errors occured by rounding
pool_fee = config_data["pool_fee"]
pool_account = config_data["pool_account"]
payment_fee = config_data["payment_fee"]
pplns_interval = config_data["pplns_interval"]   # in secs

wallet_jsonrpc_ip = config_data["wallet_jsonrpc_ip"]
wallet_jsonrpc_port = config_data["wallet_jsonrpc_port"]

wallet_mining_ip = config_data["wallet_mining_host"]
wallet_mining_port = config_data["wallet_mining_port"]
main_db_file = config_data["main_db_file"]

# other configs
orphan_age_limit = 20   # after how many blocks should the pool mark a block as orphan
payment_prec = 4
maturation_time = 10        # in blocks