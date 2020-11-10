# import keys
from Crypto.PublicKey import RSA
# deserialize data
import pickle


class Wallet:
'''
Class to represent a wallet for convenience
'''

    def __init__(self, display_name):
         wfile = 'wallets/' + display_name + '.wallet'
         with open(wfile, 'rb') as f:
             self.wallet = pickle.load(f)


    def _get_key(ps):
        txt = self.wallet[ps]
        return RSA.import_key(txt)


    def get_sk():
        return _get_key('sk')


    def get_pk():
        return _get_key('pk')
