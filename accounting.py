'''
Accounting simply crawls through the blocks and sums up mining fees and transactions.

It assumes that all blocks are valid. Checking validity is the responsibility of ledger
'''


import pickle


acts = None


class NonExistentAccountError(Exception):
    'If an account does not exist'


def _update_act_balance(disp, amt):
    global acts
    for act in acts:
        if disp in act.values():
            act['balance'] += amt


def available_balance(account, amount, pending_posts):
    global acts
    avail = -1.0
    # get available balance from blocks
    for act in acts:
        if account in act.values():
            avail = act['balance']
    # subtract pending transactions from available funds so you can't overdraft in a single block
    for post in pending_posts:
        p = post.post_payload
        payer = p.poster_public_register['display-name']
        if account == payer:
            avail -= p.transaction['amount']
    # the only way avail can be None is if no account name was found
    if avail is None:
        raise NonExistentAccountError
    return avail >= amount


def load_accounts(blocks):
    global acts
    pub_reg = 'public_register'
    with open(pub_reg, 'rb') as f:
        public_register = pickle.load(f)

    # ignore the first block, which is there only to bootstrap the rest
    blocks = blocks[1:]

    acts = public_register['accounts']

    for block in blocks:
        # miner gets awarded 1 as a reward
        miner = block.miner_id
        _update_act_balance(miner, 1.0)

        for post in block.posts:
            payload = post.post_payload
            try:
                payee = payload.transaction['payee']['display-name']
            # not all posts contain transactions, which is fine
            except TypeError:
                payee = ''
            if not payee == '':
                pending_amt = payload.transaction['amount']
                _update_act_balance(payee, pending_amt)
                payor = payload.poster_public_register['display-name']
                _update_act_balance(payor, -1.0 * pending_amt)


def get_accounts():
    global acts
    return acts
