# Blockchain and crypto currency implementation in python3
import functools
from hash_util import hash_block, hash_string_256
from collections import OrderedDict
import json

MINING_REWARD = 10

genesis_block = {
    'previous_block_hash':'',
    'index':0,
    'transactions': [],
    'proof': 10
}
blockchain = [genesis_block]
open_transactions=[]
owner = 'Max'
participants={"Max"}

def load_data():
    with open('Blockchain_data.txt', 'r') as file:
        file_content = file.readlines()
        global blockchain 
        global open_transactions
        blockchain = json.loads(file_content[0][:-1])
        #using update_blockchain to convert transactions to OderedDict to make sure hash comparison wont fail
        updated_blockchain = []
        for block in blockchain:
            updated_block ={
                'previous_block_hash': block['previous_block_hash'],
                'index':block['index'],
                'transactions': [ OrderedDict([('sender', tx['sender']), ('receiver', tx['receiver']), ('amount', tx['amount'])]) for tx in block['transactions']],
                'proof': block['proof']
            }
            updated_blockchain.append(updated_block)
        blockchain = updated_blockchain
        open_transactions = json.loads(file_content[1])
        #using updated_open_transaction to convert open_transactions to OderedDict to make sure hash comparison wont fail
        updated_open_transactions = []
        for tx in open_transactions:
            updated_tx = OrderedDict([('sender', tx['sender']), ('receiver', tx['receiver']), ('amount', tx['amount'])])
            updated_open_transactions.append(updated_tx)
        open_transactions = updated_open_transactions

load_data()

def get_last_blockchain_value():
    """ Return last block value from the blockchain.

    Returns:
        last block of the blockchain
    """
    if len(blockchain) < 1:
        return [1]
    return blockchain[-1]

def add_transaction(receiver, sender=owner, amount=1.0):
    """ Add a transaction to the open transaction list
    
    Args:
        sender: sender of the coins
        receiver: receiver of the coins
        amount: the amount of coins sent with transaction(default=1.0)
    """
    # transaction = {'sender':sender, 'receiver': receiver, 'amount':amount}
    # Using orderDict instead of Dictionary to make sure hashing wont affect, 
    # by default Dict is unordered, may result in diff hash for the same set of records
    transaction = OrderedDict([('sender', sender), ('receiver', receiver), ('amount', amount)])
    if verify_transaction(transaction):
        open_transactions.append(transaction)    
        participants.add(sender)
        participants.add(receiver)
        save_data()
        return True
    else:
        return False 


def valid_proof(transactions, last_block_hash, proof):
    guess = (str(transactions) + str(last_block_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    # print(guess_hash)
    return guess_hash[:2] == '00'

def proof_of_work():
    last_block = blockchain[-1]
    last_block_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_block_hash, proof):
        proof += 1
    return proof

def save_data():
    with open('Blockchain_data.txt', 'w') as file:
        file.write(json.dumps(blockchain))
        file.write("\n")
        file.write(json.dumps(open_transactions))

def block_mine():
    last_block = blockchain[-1]
    hashed_last_block = hash_block(last_block)
    # print(hashed_last_block)
    # reward_transaction = {
    #     'sender' : 'MINING',
    #     'receiver' : owner,
    #     'amount' : MINING_REWARD
    # }
    reward_transaction = OrderedDict(([('sender','MINING'), ('receiver', owner), ('amount', MINING_REWARD)]))
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    proof = proof_of_work()
    block = {
        'previous_block_hash':hashed_last_block,
        'index':len(blockchain),
        'transactions': copied_transactions,
        'proof' : proof
    }
    blockchain.append(block)
    return True

def verify_transaction(transaction):
    """ Validates the transcaction.

    Retuns:
        True - if sender have enough money to send
        False - if sender dont have enough money to send
    """
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']

def validate_blockchain():
    """ Validates the blockchain.

    Retuns:
        True - if blockchain is valid
        False - if blockchian is not valid
    """
    for (index,block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_block_hash'] != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['previous_block_hash'], block['proof']):
            print("Invlaid proof of work")
            return False
    return True


def get_balance(participant):
    tx_sender = [[  tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [ tx['amount'] for tx in open_transactions if tx['sender'] == participant ]
    tx_sender.append(open_tx_sender)
    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum,tx_sender, 0)
    # amount_sent = 0
    # for tx in tx_sender: 
    #     if len(tx) > 0:
    #         amount_sent += tx[0]

    tx_recipient = [[ tx['amount'] for tx in block['transactions'] if tx['receiver'] == participant ] for block in blockchain]
    amount_recieved = functools.reduce( lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt)>0 else tx_sum, tx_recipient, 0)
    # amount_recieved = 0
    # for tx in tx_recipient: 
    #     if len(tx) > 0:
    #         amount_recieved += tx[0]
    
    return amount_recieved - amount_sent

def get_transaction_value():
    """ Get transaction information(recipient, amount) from the user.

    Returns:
        tuple(receiver, amount) 
    """
    tx_receiver = input("Enter recipient name: ")
    tx_amount = float(input("Enter your transaction amount: "))
    return (tx_receiver, tx_amount)

def print_blockchain():
    """ Prints entire blockchain.
    """
    print("Printing blockchain")
    for block in blockchain:
        print(block)
    print("Done!")

def get_user_choice():
    """ Takes user input for choice 
    
    Retuns:
        user choice
    """

    return input('Your choice: ')

while True:
    print("\nPlease choose")
    print("1. Add a transaction value")
    print("2. Mine a block")
    print("3. Print blockchian")
    print("4. Print participants")
    print("5. Hack the planet")
    print("6. Quit")
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print("Transaction added.")
        else:
            print("Transaction failed, insufficient balance!!")
        
    elif user_choice == '2':
        if block_mine():
            print('Mining successfull!!!')
            open_transactions = []
            save_data()

    elif user_choice == '3':
        print_blockchain()

    elif user_choice == '4':
        print(participants)

    elif user_choice == '5':
        if len(blockchain) > 0:
            blockchain[0]['proof'] = 2

    elif user_choice == '6':
        break

    else:
        print("Invalid choice")

    if not validate_blockchain():
        print('Invalid Chain!!!')
        break

    print("Balance of {} is : {:6.2f}".format('Max',get_balance('Max')))

