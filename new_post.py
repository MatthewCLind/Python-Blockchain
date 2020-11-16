'''
A "post" is what is used to add information to new blocks being added to the blockchain.
In general, it contains two types of information, arbitrary data, and transactional information for exchanging currency.

Arbitrary data is an option, because this is where a user may publicly agree to contractual terms and the like.
'''

# pkcs1_15 is the "signing object" we use to cryptographically sign data using wallet key-pairs
from Crypto.Signature import pkcs1_15
# SHA384 is a cryptographic hashing algorithm that we use for signing
from Crypto.Hash import SHA384
# RSA is how we use the key-pairs (mostly importing, then using the pkcs1_15 signer above)
from Crypto.PublicKey import RSA
# pickle serializes / deserializes data such as wallets and the ledger
import pickle
# ledger is where all of the classes and functions live for accessing and contributing to the blockchain
import ledger
# wallet objects just make accessing a wallet much easier
from wallet import Wallet


# convenience function for getting yes/no input from user
def yn_ans(query):
    yn = ''
    while yn != 'y' and yn != 'n':
        yn = input(query)
    return yn


# load in the wallet
disp_name = input('What is your display name?\n\t> ')
user_wallet = Wallet(disp_name)

payee = ''
amount = 0.0
data = None
yn = ''
yn = yn_ans('Would you like to pay someone? [ y / n ] ')

# if the user wants to pay, get the payee's account info, and amount
if yn == 'y':
    payee = input('What is the display name of the account you want to pay?\n> ')
    amount = input('How much?\n> ')
    amount = float(amount)

# if the user wants to add data (in this case only keyboard inputs), colect it
yn = yn_ans('Do you want to add some data? [ y / n ] ')
if yn == 'y':
    data = input('What is the data you want to add?\n> ')


# load the public registry
pub_reg = 'public_register'
with open(pub_reg, 'rb') as f:
    public_register = pickle.load(f)

# search for, and load the public account of the payee
payee_pub = ''
poster_pub = ''
for acct in public_register['accounts']:
    if payee in acct.values():
        payee_pub = acct
    elif disp_name in acct.values():
        poster_pub = acct


# load in the secret and private keys for signing
sk = user_wallet.get_sk()
pk = user_wallet.get_pk()

# turn the post data into a post payload object, this is what is hashed and signed
post_payload = ledger.generate_post_payload(poster_pub, payee_pub, amount, data)
# serialize the post_payload in order to sign it
post_bytes = pickle.dumps(post_payload)

# sign the post payload
# create a new signer object with the secret key
signer = pkcs1_15.new(sk)
# create a new hasher object
hasher = SHA384.new()
# hash the post payload data
hasher.update(post_bytes)
# create the signature
signature = signer.sign(hasher)
# make sure the signature checks out by creating a new signer object, val, and validating
val = pkcs1_15.new(pk)
# if no errors are raised, this is successful and the signature is valid
val.verify(hasher, signature)

# submit the post to the ledger, will be added to pending_posts file
ledger.submit_post(post_payload, signature)
