# for serializing / deserializing data
import pickle
# for signing
from Crypto.Signature import pkcs1_15
# hasher for signatures
from Crypto.Hash import SHA384
# hasher for blocks
from Crypto.Hash import SHA256
# for loading / exporting public and secret keys
from Crypto.PublicKey import RSA


# variable used globally for accessing ledger data
ledger = None


class _Post_Payload:
    '''
    Class for containing post data
    '''

    def __init__(self, block_id, poster_public_register, payee_public_register, amount, data):
        self.block_id = block_id
        self.poster_public_register = poster_public_register
        self.transaction = {'payee': payee_public_register,'amount': amount} # payee will be a public wallet object
        self.data = data


class _Post:
    '''
    Class for posts which contain a _Post_Payload object and a valid signature
    '''

    def __init__(self, post_payload, signature):
        self.post_payload = post_payload
        self.signature = signature


class _Work_Proof:
    '''
    Class for containing the proof of work done by a miner
    work_proof is a SHA256 hash of the _Block_Payload which begins with 5 zero bytes, which is the definition of "work"
    '''

    def __init__(self, miner_id, miner_pk, proof):
        self.miker_id = miner_id
        self.miner_pk = miner_pk
        self.work_proof = proof # signed hash of Block_Payload


class _Block:
    '''
    Class which represents a block on the chain.
    The miner will create this object and keep updating the work string until the SHA256 hash produces 5 leading zeroes
    A list of Blocks is the blockchain, which is maintained in the ledger file
    '''

    def __init__(self, block_id, previous_block_hash, posts, miner_id, miner_pk):
        # block IDs are simply the integers in order
        self.block_id = block_id
        # the previous block hash is included for verifying that this block payload is truly the next in sequence
        self.previous_block_hash = previous_block_hash
        self.posts = posts
        self.miner_id = miner_id
        self.miner_pk = miner_pk


    def update_work(self, work_str):
        self.work = work_str


def retrieve_ledger():
    # open the ledger file
    # read in the contents
    # unpickle the ledger
    with open('ledger', 'rb') as f:
        l = pickle.load(f)
    return l


def check_ledger():
    # read through the blocks one at a time
    # check the previous block hashes to this block's hash (except first block)
    # check the work has 5 zeroes and hashes
    pass


def save_ledger():
    # pickle the ledger
    # save it to file
    with open('ledger', 'wb') as f:
        pickle.dump(ledger, f)


def get_current_block_id(ledger):
    # return the id of the the newest block + 1
    return len(ledger['blocks']) + 1


def generate_post_payload(poster_public_register, payee_public_register, amount, data):
    # block_id is always added so signatures are tied uniquely to this post, otherwise a signature could be re-used by duplicating an identical post
    block_id = get_current_block_id(ledger)
    post_payload = _Post_Payload(block_id, poster_public_register, payee_public_register, amount, data)
    return post_payload


def add_post_to_pending_posts(new_post):
    global ledger
    # add the new post to the list of pending posts, which will be collected and added to the next mined block
    ledger['pending-posts'].append(new_post)
    save_ledger()


def get_pending_posts():
    return ledger['pending-posts']


def get_prev_block_hash():
    # get the previous block from the ledger
    prev_block = ledger['blocks'][-1]
    # convert it into bytes for hashing
    block_bytes = pickle.dumps(prev_block)
    # create new SHA256 hasher
    hasher = SHA256.new()
    # process the block byes
    hasher.update(block_bytes)
    # retrieve the hash
    block_hash = hasher.digest()
    return block_hash


def create_block():
    # get the active block id number
    block_id = get_current_block_id()
    # get the hash of the previous block
    prev_block_hash = get_prev_block_hash()
    # get all pending posts
    posts = get_pending_posts()
    # create the _Block object
    block_payload = _Block_Payload(block_id, previous_block_hash, posts)
    return block_payload


def validate_post_payload(post_payload, signature):
    # make sure the signature works
    # make sure the payor has sufficient funds
    pass


def submit_post(post_payload, signature):
    # validate the post_payload data
    validate_post_payload(post_payload, signature)
    # create the bytes representation of the data
    post_payload_bytes = pickle.dumps(post_payload)
    # create a sha384 hasher
    hasher = SHA384.new()
    # process the post_payload data
    hasher.update(post_payload_bytes)
    # retrieve the public key from the signer
    poster_pk = post_payload.poster_public_register['pk']
    poster_pk = RSA.import_key(poster_pk)
    # create a signer object
    validator = pkcs1_15.new(poster_pk)
    # call verify with hasher and signature to validate. No errors = valid
    validator.verify(hasher, signature)

    # create a new _Post object
    new_post = _Post(post_payload, signature)
    # add the post to pending posts
    add_post_to_pending_posts(new_post)



def clear_pending_posts():
    global ledger
    ledger['pending-posts'] = []


def add_block_to_chain(solved_block):
    # verify that the block is correct

    # delete old pending posts
    # note that this creates race conditions where new posts added after the miner began will be lost
    # to mitigate the race condition, later on a lock on the pending posts list can be implemented
    clear_pending_posts()

    # append the block to the chain
    ledger['blocks'].append(solved_block)

    # save the updated ledger
    save_ledger()


def create_block(miner_id, miner_pk):
    global ledger
    block_id = get_current_block_id(ledger)
    previous_block_hash = get_prev_block_hash()
    posts = ledger['pending-posts']
    pk_exp = miner_pk.export_key()
    new_block = _Block(block_id, previous_block_hash, posts, miner_id, pk_exp)
    return new_block


def first_block():
    global ledger
    bid = 0
    pbh = b''
    posts = []
    mid = b''
    mpk = b''
    return _Block(bid, pbh, posts, mid, mpk)


def get_blocks():
    global ledger
    return ledger['blocks']


# load ledger data to ledger global
ledger = retrieve_ledger()
print(ledger)
