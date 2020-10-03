from Crypto.PublicKey import RSA  # pip install pycryptodome
import pickle

wallet_dict = {'display-name':'','pk':None,'sk':None,'currency': 0.0} #python dict representing a wallet

DISPLAY_NAME_PROMPT = 'Please input your desired display name:\n\t> '
display_name = input(DISPLAY_NAME_PROMPT)

outfile = 'wallets/' + display_name + '.wallet' # there is no checking for collisions, so have a unique name please

key = RSA.generate(2048)  # 2048 is modulus n, which is number of bits in the RSA alorithm. More is better encryption

wallet_dict['display-name'] = display_name
wallet_dict['sk'] = key.export_key()
wallet_dict['pk'] = key.publickey().export_key()

print(wallet_dict)

with open(outfile,'wb') as f:
    pickle.dump(wallet_dict, f)

public_register_fn = '../ledger/public_register'
public_registration = {'display-name':display_name, 'public-key':key.publickey().export_key()}
with open(public_register_fn, 'rb') as f:
    public_register = pickle.load(f)
#public_register = {'accounts':[]}
public_register['accounts'].append(public_registration)
with open(public_register_fn, 'wb') as f:
    pickle.dump(public_register, f)
