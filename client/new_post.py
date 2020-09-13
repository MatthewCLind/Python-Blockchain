import sys
sys.path.append('../common')
import wallet_functions


wallet = wallet_functions.retrieve_wallet()
pk, sk = wallet_functions.load_keys(wallet)
