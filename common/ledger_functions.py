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


def verify_posts(posts):
    pass #in future, implement a check that the client produced a valid post

def _save_posts(posts):
    posts = verify_posts(posts)
    _save_dict_to_file(posts, PENDING_POSTS_PATH)


def get_pending_posts():
    posts = _load_file_to_dict(PENDING_POSTS_PATH)
    return posts


def add_post(post):
    posts = get_pending_posts()
    posts['posts'].append(post)
    _save_posts(posts)


def get_public_register():
    return _load_file_to_dict(PUBLIC_REGISTER_PATH)


def get_public_key_str(uid):
    pk = None
    pr = get_public_register()
    for account in pr['accounts']:
        if account['display-name'] == uid:
            pk = account['public-key']
    return pk


def add_ledger_block(block):
    ledger = get_ledger()
    ledger['blocks'].append(block)
    _save_ledger(ledger)
