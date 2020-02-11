
is_release = True

if is_release:
    wallet_path = "C:\\Users\\Administrator\\Documents\\crypto\\MicroCoin\\MicroCoin\\MicroCoinWallet.exe"
else:
    wallet_path = "C:\\Program Files (x86)\\MicroCoin\\MicroCoinWallet.exe"

orphan_age_limit = 20   # after how many blocks should the pool mark a block as orphan

payment_fee_to_pool = 0.0001        # this fee will be sent to pool address in order to prevent tx errors occured by rounding