import json


LEDGER_PATH = '../ledger/ledger'
PENDING_POSTS_PATH = '../ledger/pending_posts'
PUBLIC_REGISTER_PATH = '../ledger/public_register'


def _load_file_to_dict(fn):
    with open(fn, 'r') as f:
        la = f.read()
        d = json.loads(la)
    return d


def _save_dict_to_file(d, fn):
    with open(fn, 'w') as f:
        ds = json.dumps(d, indent=4)
        f.write(ds)


def get_ledger():
    return _load_file_to_dict(LEDGER_PATH)


def _save_ledger(ledger):
    _save_dict_to_file(ledger, LEDGER_PATH)


def get_pending_posts():
    return _load_file_to_dict(PENDING_POSTS_PATH)


def get_public_register():
    return _load_file_to_dict(PUBLIC_REGISTER_PATH)


def add_ledger_block(block):
    ledger = get_ledger()
    ledger['blocks'].append(block)
    _save_ledger(ledger)
