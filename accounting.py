'''
Accounting simply crawls through the blocks and sums up mining fees and transactions.

It assumes that all blocks are valid. Checking validity is the responsibility of ledger
'''

import ledger
import pickle

acts = None

def update_act_balance(disp, amt):
    global acts
    print('disp: ', disp)
    for act in acts:
        if disp in act.values():
            act['balance'] += amt


pub_reg = 'public_register'
with open(pub_reg, 'rb') as f:
    public_register = pickle.load(f)


blocks = ledger.get_blocks()
# ignore the first block, which is there only to bootstrap the rest
blocks = blocks[1:]

acts = public_register['accounts']

for block in blocks:
    # miner gets awarded 1 as a reward
    miner = block.miner_id
    update_act_balance(miner, 1.0)

    for post in block.posts:
        payload = post.post_payload
        payee = payload.transaction['payee']['display-name']
        print("\n\nPayee:",payee,'\n')
        if not payee == '':
            pending_amt = payload.transaction['amount']
            update_act_balance(payee, pending_amt)
            payor = payload.poster_public_register['display-name']
            update_act_balance(payor, -1.0 * pending_amt)


print(acts)
