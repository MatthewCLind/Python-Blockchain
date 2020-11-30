# Overview
This is a blockchain model I built to learn how blockchain works.

If a Ford is a type of car, and BitCoin is a type of blockchain, then this is a gokart. Right now it starts and runs, but it very well might break down if you tap the brakes while turning left if your seatbelt isn't buckled.

In general, users will do the following:
1. Create one or more wallets (user credentials) using `create_wallet.py`
2. Add some posts to the current block using `new_post.py`
3. Mine the block using `mine_block.py`
4. View the blockchain using `reporting.py`

Feel free to try it out and mine yourself some 'Coin. Then trade it to yourself.

# Future Development
1. Could use a lot more testing
2. Separate the frontend from the backend
3. GUI?
4. The big one is to make this work over a network in a decentralized fashion. That way we can mess around with learning how distributed validation builds trust in the ledger, and how the system can be overtaken when bad actors gain control of the majority of computing power in the network.
