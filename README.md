# MicroCoin mining pool
 This is a complete pool engine for the MicroCoin (MCC) ecosystem.
 This is a work in progess hobby project. Use it at your own risk. I don't take any responsibility for any loss.
 The frontend is not ready yet.
 Use it on Linux based systems, Windows wallet communication is slow, you won't be happy with that.
 Tested on Ubuntu 18.04.
 
# Features
 - supports 2 mining difficulties (can be extended):
  - difficulty 1 on port 3333 for GPUs
  - difficulty 32 on port 3334 for ASICs
 - supports Pascal hashing algo
 - payout at every block
 - easy to install
 # Get started
 Detailed tutorial will be available soon.
 
- download MicroCoin daemon 1.0.3.2.: https://github.com/MicroCoinHU/MicroCoin-Daemon/releases/tag/v1.0.3.2
  Later versions have a bug in sending payments. Will be fixed soon.
- unpack
- set executable permission
- run
- wait for daemon sync, it can take hours
```
wget https://github.com/MicroCoinHU/microcoind/files/2408042/x86_x64-linux-openssl-1.1.tar.gz
tar -xf x86_x64-linux-openssl-1.1.tar.gz
chmod +x microcoind
nohup ./microcoind -r &
```
- clone the pool repo
- set parameters in config.txt. For default settings set only the first 2 parameters:
 - pool_fee: your pool fee in percentage
 - pool_account: the account where your pool fee will be sent to
- run the pool
```
git clone https://github.com/tamasvegera/protopool
cd protopool
vim config.txt
nohup python3 ./_main.py &
```
