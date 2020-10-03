import pickle
import os


class _Post_Payload:

    def __init__(self, block_id, poster_wallet, payee_wallet, amount, data):
        self.block_id = block_id
        self.poster_wallet = poster_wallet
        self.transaction = {'payee': payee_wallet,'amount': amount} # payee will be a public wallet object
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


class Ledger:

    def __init__(self):
        self.ledger = retrieve_ledger()


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


    def get_current_block_id():
        # return the id of the the newest block + 1


    def new_post_payload(block_id, poster_wallet, payee_wallet, amount, data):
