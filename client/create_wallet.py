from Crypto.PublicKey import RSA  # pip install pycryptodome
import json

wallet_dict = {'display-name':'','public-key':'','secret-key':'','currency':0.0} #python dict representing a wallet

DISPLAY_NAME_PROMPT = 'Please input your desired display name:\n\t> '
display_name = input(DISPLAY_NAME_PROMPT)

outfile = 'wallets/' + display_name + '.wallet' # there is no checking for collisions, so have a unique name please

key = RSA.generate(2048)  # 2048 is modulus n, which is number of bits in the RSA alorithm. More is better encryption

wallet_dict['display-name'] = display_name
wallet_dict['public-key'] = key.publickey().export_key().decode('utf-8')  # json requires strings, not bytes, so decode the bytes given by the RSA key object
wallet_dict['secret-key'] = key.export_key().decode('utf-8')
wallet_json = json.dumps(wallet_dict, indent=4)

with open(outfile,'w') as f:
    f.write(wallet_json)


public_register_fn = '../ledger/public_register'
public_registration = {'display-name':display_name, 'public-key':wallet_dict['public-key']}
with open(public_register_fn, 'r') as f:
    public_register = json.loads(f.read())

public_register['accounts'].append(public_registration)
pr_json = json.dumps(public_register, indent=4)
with open(public_register_fn, 'w') as f:
    f.write(pr_json)
