from Crypto.Hash import SHA256 as sha
from Crypto.Random import get_random_bytes as rand
from timeit import timeit
import json
import sys
sys.path.append('../common')
import wallet_functions
import ledger_functions


REQUIRED_ZEROES = 5


def leading_zeroes(hash_out):
    leading_zeroes_cnt = 0
    for byte in hash_out:
        if byte == '0':
            leading_zeroes_cnt += 1
        else:
            break
    return leading_zeroes_cnt


def is_hashed(hash_out, num_zeroes = REQUIRED_ZEROES):
    return leading_zeroes(hash_out) == num_zeroes


def solve_block(block, max_attempts=1000000):
    successful_hash = False
    attempts = 0
    biggest_chain = 0
    while not successful_hash:
        attempts += 1
        guess = str(rand(20))
        block['block-validation']['proof-of-work'] = guess
        block_str = create_block_str(block)
        sha_obj = sha.new(data=block_str)
        guess_hash = sha_obj.hexdigest()
        solved = is_hashed(guess_hash)
        successful_hash = solved or attempts > max_attempts
        lz = leading_zeroes(guess_hash)
        if lz > biggest_chain:
            biggest_chain = lz

    print('guess: ', guess)
    print('biggest chain: ', biggest_chain)
    print('number of guesses: ', attempts)
    print('leading zeroes: ', leading_zeroes(guess_hash))
    print('hash[0]: ',guess_hash[0] == '0')
    print('hash: ',guess_hash)
    if not solved:
        block = None
    return block


def create_block_str(block_dict):
    block_s = json.dumps(block_dict).encode('utf-8')
    return block_s


def hash_block_dict(block):
    block_s = create_block_str(block)
    sha_obj = sha.new(data=block_s)
    block_hash = sha_obj.hexdigest()
    return block_hash


def assemble_new_block(prev_block, prev_block_hash, pending_posts, pk, display_name):
    new_block = {'block-validation':{}}
    new_block_id = prev_block['block-id'] + 1
    new_block['block-id'] = new_block_id
    new_block['previous-hash'] = prev_block_hash
    new_block['ledger-posts'] = pending_posts['posts'][:1000]
    new_block['block-validation']['worker'] = pk.publickey().export_key().decode('utf-8')
    new_block['block-validation']['worker-display-name'] = display_name
    return new_block


wallet = wallet_functions.retrieve_wallet()
pk, sk = wallet_functions.load_keys(wallet)
display_name = wallet['display-name']

ledger = ledger_functions.get_ledger()
pending_posts = ledger_functions.get_pending_posts()

blocks = ledger['blocks']
prev_block = blocks[-1]
prev_block_hash = hash_block_dict(prev_block)

new_block = assemble_new_block(prev_block, prev_block_hash, pending_posts, pk, display_name)

solved_block = solve_block(new_block)
print(solved_block)

if solved_block is not None:
    ledger_functions.add_ledger_block(solved_block)
