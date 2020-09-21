import pickle
import os

class _Post_Payload:

    def __init__(self, block_id):
        self.block_id = block_id
        self.transaction = {'payee':None,'amount':0.00} # payee will be a public wallet object
        self.data = None


    def transaction(self, payee, amount):
        self.transaction['amount'] = amount
        self.transaction['payee'] = payee


class Post:

    def __init__(self, poster, block_id):
        self.poster = poster_wallet # poster wallet is a public wallet
        self.payload = _Post_Payload(block_id)
        self.signature = None

    def transaction(self, payee, amount):
        self.payload.transaction(payee, amount)

    def get_payload_bytes():
        return pickle.dumps(self.payload)

    def sign_post(signature):
        self.signature = signature


def _Work_Proof:

    def __init__(self):
        self.worker = None # will be a public wallet
        self.work_proof = None # signed hash of Block_Payload

    def record_work(self, worker, proof):
        self.worker = worker
        self.work_proof = proof


def _Block_Payload:
    def __init__(self, block_id, previous_block_hash, posts):
        self.block_id = block_id
        self.previous_block_hash = previous_block_hash
        self.posts = posts


def Block:

    def __init__(self, previous_hash
