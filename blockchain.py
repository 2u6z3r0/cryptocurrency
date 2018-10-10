# Blockchain and crypto currency implementation in python3
import functools

MINING_REWARD = 10

genesis_block = {
    'previous_block_hash':'',
    'index':0,
    'transactions': []
}
blockchain = [genesis_block]
open_transactions=[]
owner = 'Max'
participants={"Max"}

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
    transaction = {'sender':sender, 'receiver': receiver, 'amount':amount}
    if verify_transaction(transaction):
        open_transactions.append(transaction)    
        participants.add(sender)
        participants.add(receiver)
        return True
    else:
        return False 

def hash_block(block):
    return '-'.join([str(block[key]) for key in block])

def block_mine():
    last_block = blockchain[-1]
    hashed_last_block = hash_block(last_block)
    print(hashed_last_block)
    reward_transaction = {
        'sender' : 'MINING',
        'receiver' : owner,
        'amount' : MINING_REWARD
    }
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_block_hash':hashed_last_block,
        'index':len(blockchain),
        'transactions': copied_transactions
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
        elif block['previous_block_hash'] != hash_block(blockchain[index - 1]):
            return False
    return True


def get_balance(participant):
    tx_sender = [[  tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [ [tx['amount']] for tx in open_transactions if tx['sender'] == participant ]
    tx_sender.extend(open_tx_sender)

    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + tx_amt[0] if len(tx_amt) > 0 else 0,tx_sender, 0)
    # amount_sent = 0
    # for tx in tx_sender: 
    #     if len(tx) > 0:
    #         amount_sent += tx[0]

    tx_recipient = [[ tx['amount'] for tx in block['transactions'] if tx['receiver'] == participant ] for block in blockchain]
    amount_recieved = functools.reduce( lambda tx_sum, tx_amt: tx_sum + tx_amt[0] if len(tx_amt)>0 else 0, tx_recipient, 0)
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
            open_transactions = []
    elif user_choice == '3':
        print_blockchain()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if len(blockchain) > 0:
            blockchain[0] = {
                'previous_block_hash':'',
                'index':0,
                'transaction': {'sender': 'Sai', 'receiver': 'Max', 'amount':100}
            }
    elif user_choice == '6':
        break
    else:
        print("Invalid choice")
    print("Balance of {} is : {:6.2f}".format('Max',get_balance('Max')))
    if not validate_blockchain():
        print('Invalid Chain!!!')
        break

