'''
This script generates a new wallet for use with the rest of the block chain.
The wallet contains a user's ID, their public key, and their secret key, as well as currency amount for later convenience.

This script also generates a public registry account, which is the wallet without the secret key. This is saved to the public registry, which allows all users to access each others credentials for sending POSTS (including currency)

Note that this script will generate the key-pair and simply save it to your harddrive, which is not at all secure, it would be possible to password protect this information, but that is a hassle and not wirth it for this demo program.
'''


# RSA is the public/private key pair which we'll use as the basis of our authentication
from Crypto.PublicKey import RSA  # pip install pycryptodome

# pickle serializes simple python objects so we can later save them as binary files
import pickle

# python dictionary representing a wallet
# pk = public key
# sk = secret key (private key)
wallet_dict = {'display-name':'','pk':None,'sk':None,'currency': 0.0}

# have the user choose their display name, which is what we use as the UID to make things easier to remember
DISPLAY_NAME_PROMPT = 'Please input your desired display name:\n\t> '
display_name = input(DISPLAY_NAME_PROMPT)

# create a keypair
key = RSA.generate(2048)  # 2048 is modulus n, which is number of bits in the RSA alorithm. More is better encryption

# fill in display name
wallet_dict['display-name'] = display_name

# "export_key" just turns the key into something we can save, when using a wallet in the future, undo this with "import_key()"
wallet_dict['sk'] = key.export_key()

# same as above, but get the public key
wallet_dict['pk'] = key.publickey().export_key()

# the new wallet will be saved in its own file in the "wallets" directory
outfile = 'wallets/' + display_name + '.wallet' # there is no checking for collisions, so have a unique name please

# write out the wallet to the wallet file
# write mode is binary
with open(outfile,'wb') as f:
    # pickle.dump serializes and writes all at once
    pickle.dump(wallet_dict, f)

# the public register is a dictionary of public info
# importantly, it contains a list of all public wallet info without their secret keys
public_register_fn = 'public_register'
public_registration = {'display-name':display_name, 'pk':key.publickey().export_key(), 'balance':0.0}

# here we load in the public register from its pickled file contents
# must open in binary mode for pickle
with open(public_register_fn, 'rb') as f:
    # first we must load in the list of all registrations
    public_register = pickle.load(f)

# now pickle and write out the public register with its new account
# the list of public wallets is found under 'accounts'
public_register['accounts'].append(public_registration)
with open(public_register_fn, 'wb') as f:
    # write the updated public register back to the file
    pickle.dump(public_register, f)
