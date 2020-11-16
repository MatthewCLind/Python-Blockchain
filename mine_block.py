from Crypto.Hash import SHA256 as sha
from Crypto.Random import get_random_bytes as rand
from wallet import Wallet
import ledger
from timeit import timeit
import pickle


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


def mine_block(new_block, max_attempts=10000000):
    done = False
    attempts = 0
    biggest_chain = 0
    while not done:
        attempts += 1
        guess = str(rand(20))
        new_block.update_work(guess)
        block_bytes = pickle.dumps(new_block)
        sha_obj = sha.new(data=block_bytes)
        guess_hash = sha_obj.hexdigest()
        solved = is_hashed(guess_hash)
        done = solved or (attempts > max_attempts)
        lz = leading_zeroes(guess_hash)
        if lz > biggest_chain:
            biggest_chain = lz

    print('guess: ', guess)
    print('biggest chain: ', biggest_chain)
    print('number of guesses: ', attempts)
    print('leading zeroes: ', leading_zeroes(guess_hash))
    print('hash[0]: ',guess_hash[0] == '0')
    print('hash: ',guess_hash)
    return new_block, solved


# load in the miner's wallet
display_name = input('what is your display name?\n\t')
user_wallet = Wallet(display_name)
pk = user_wallet.get_pk()
sk = user_wallet.get_sk()

# generate the block for mining
new_block = ledger.create_block(display_name, pk)

# mine the block
mined_block, success = mine_block(new_block)

if success:
    print('WE DID IT!')
    ledger.add_block_to_chain(mined_block)
