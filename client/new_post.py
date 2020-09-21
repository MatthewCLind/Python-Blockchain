import sys
sys.path.append('../common')
import wallet_functions
import ledger_functions
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA384
import json


def yn_ans(query):
    yn = ''
    while yn != 'y' and yn != 'n':
        yn = input(query)
    return yn


wallet = wallet_functions.retrieve_wallet()
pk, sk = wallet_functions.load_keys(wallet)


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


payee_pk = ledger_functions.get_public_key_str(payee)
transaction = {'payee':payee,'payee-pk':payee_pk,'amount':amount}
post={'transaction':transaction,'data':data}
post_bytes = json.dumps(post,indent=4).encode('utf-8')
signer = pkcs1_15.new(sk)
hasher = SHA384.new()
hasher.update(post_bytes)
signature = signer.sign(hasher)#.decode('utf-8','ignore')
print(signature)
print('type: ',type(signature))

#signature = str(signature)
signature = signature.decode('utf-8').replace("'",'"')
print('string signature: ',type(signature))
signature = signature.encode('utf-8')
signature = bytes(signature)
print(signature)
print('bytes signature: ',type(signature))


bs = signature
val = pkcs1_15.new(pk)
print(val.verify(hasher, bs))
