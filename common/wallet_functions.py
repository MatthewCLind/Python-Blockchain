from Crypto.PublicKey import RSA
import json
import sys


def load_wallet(wallet_name):
    wallet_name = '../client/wallets/' + wallet_name
    try:
        with open(wallet_name,'r') as f:
            raw_wallet = f.read()

        wallet = json.loads(raw_wallet)
    except FileNotFoundError:
        print('Could not find your wallet :/')
        sys.exit(0)
    return wallet


def load_keys(wallet):
    pk_b = wallet['public-key'].encode('utf-8')  # RSA key object requires byte strings, hence "encode"
    sk_b = wallet['secret-key'].encode('utf-8')

    pk = RSA.import_key(pk_b)
    sk = RSA.import_key(sk_b)

    return (pk, sk)


def retrieve_wallet():
    display_name=input('What is your display name?\n > ')
    wallet_name = display_name + '.wallet'
    wallet = load_wallet(wallet_name)
    return wallet
