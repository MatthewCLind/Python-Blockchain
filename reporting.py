import ledger
import accounting

acts = accounting.acts
with open('report.csv','w') as f:
    f.write('Accounts\n')
    f.write('Display Name,Balance\n')
    for act in acts:
        disp = act['display-name']
        bal = act['balance']
        bal = str(bal)
        line = disp + ',' + bal + '\n'
        f.write(line)


    f.write('\n\nLedger Blocks\n')
    header = 'block ID,Miner ID, Miner PK,Previous Block Hash, Work\n'
    f.write(header)

    blocks = ledger.ledger['blocks'][1:] #ignore the first block
    for block in blocks:
        block_id = str(block.block_id).rstrip()
        miner_id = str(block.miner_id).rstrip()
        miner_pk = '' # str(block.miner_pk).rstrip()
        previous_block_hash = str(block.previous_block_hash).rstrip()
        try:
            work_str = str(block.work).rstrip().replace(',','<comma>')
        except AttributeError:
            work_str = ''
        post_str = ''
        for post in block.posts:
            p = post.post_payload
            payer = p.poster_public_register['display-name']
            payee = p.transaction['payee']['display-name']
            amount = str(p.transaction['amount'])
            data = p.data
            post_str += '%s | %s | %s | %s,'%(payer, payee, amount, data)
        output = '%s,%s,%s,%s,%s,%s\n'%(block_id, miner_id, miner_pk, previous_block_hash, work_str, post_str)
        f.write(output)
