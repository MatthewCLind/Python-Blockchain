import pickle
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA384
from Crypto.PublicKey import RSA


ledger = None


class _Post_Payload:

    def __init__(self, block_id, poster_public_register, payee_public_register, amount, data):
        self.block_id = block_id
        self.poster_public_register = poster_public_register
        self.transaction = {'payee': payee_public_register,'amount': amount} # payee will be a public wallet object
        self.data = data


class _Post:

    def __init__(self, post_payload, signature):
        self.post_payload = post_payload
        self.signature = signature


class _Work_Proof:

    def __init__(self, worker_wallet, proof):
        self.worker = worker_wallet # will be a public wallet
        self.work_proof = proof # signed hash of Block_Payload


class _Block_Payload:

    def __init__(self, block_id, previous_block_hash, posts):
        self.block_id = block_id
        self.previous_block_hash = previous_block_hash
        self.posts = posts


class _Block:

    def __init__(self, block_payload, work_proof):
            self.block_payload = block_payload
            self. work_proof = work_proof


def retrieve_ledger():
    # open the ledger file
    # read in the contents
    # unpickle the ledger
    # check the ledger for corruption


def check_ledger():
    # read through the blocks one at a time
    # check the previous block hashes to this block's hash (except first block)
    # check the work has 5 zeroes and hashes


def save_ledger():
    # check the ledger
    # pickle the ledger
    # save it to file


def get_current_block_id(ledger):
    # return the id of the the newest block + 1
    return len(ledger['blocks']) + 1


def generate_post_payload(poster_public_register, payee_public_register, amount, data):
    block_id = get_current_block_id(ledger)
    post_payload = _Post_Payload(block_id, poster_public_register, payee_public_register, amount, data)
    return post_payload


def add_post_to_current_block(new_post):
    global ledger
    ledger['pending posts'].append(new_post)


def submit_post(post_payload, signature):
    # make sure the signature is all good
    post_payload_bytes = pickle.dumps(post_payload)
    hasher = SHA384.new()
    hasher.update(post_payload_bytes)
    poster_pk = post_payload.poster_public_register['pk']
    poster_pk = RSA.import_key(poster_pk)
    validator = pkcs1_15.new(poster_pk)
    validator.verify(hasher, signature)

    # no errors means the signature was legit
    new_post = _Post(post_payload, signature)
    add_post_to_current_block(new_post)


ledger = retrieve_ledger()
