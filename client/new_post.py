from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA384
from Crypto.PublicKey import RSA
import pickle
import sys
sys.path.append('../ledger')
from ledger import *


def yn_ans(query):
    yn = ''
    while yn != 'y' and yn != 'n':
        yn = input(query)
    return yn


disp_name = input('What is your display name?\n\t> ')
wfile = 'wallets/' + disp_name + '.wallet'
with open(wfile, 'rb') as f:
    wallet = pickle.load(f)

payee = ''
amount = 0.0
data = None
yn = ''
yn = yn_ans('Would you like to pay someone? [ y / n ] ')

if yn == 'y':
    payee = input('What is the display name of the account you want to pay?\n> ')
    amount = input('How much?\n> ')
    amount = float(amount)

yn = yn_ans('Do you want to add some data? [ y / n ] ')
if yn == 'y':
    data = input('What is the data you want to add?\n> ')


pub_reg = '../ledger/public_register'
with open(pub_reg, 'rb') as f:
    public_register = pickle.load(f)
for acct in public_register['accounts']:
    if payee in acct.values():
        payee_pub = acct
    elif disp_name in acct.values():
        poster_pub = acct


ssk = wallet['sk']
sk = RSA.import_key(ssk)
spk = wallet['pk']
pk = RSA.import_key(spk)

post_payload = generate_post_payload(poster_pub, payee_pub, amount, data)
post_bytes = pickle.dumps(post_payload)

signer = pkcs1_15.new(sk)
hasher = SHA384.new()
hasher.update(post_bytes)
signature = signer.sign(hasher)
print(signature)
print('type: ',type(signature))
val = pkcs1_15.new(pk)
print(val.verify(hasher, signature))

submit_post(post_payload, signature)
