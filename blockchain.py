# Blockchain and crypto currency implementation in python3

genesis_block = {
    'previous_block_hash':'',
    'index':0,
    'transaction': []
}
blockchain = [genesis_block]
open_transactions=[]
owner = 'Max'

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
    open_transactions.append(transaction)    

def hash_block(block):
    return '-'.join([str(block[key]) for key in block])

def block_mine():
    last_block = blockchain[-1]
    hashed_last_block = hash_block(last_block)
    print(hashed_last_block)
    
    block = {
        'previous_block_hash':hashed_last_block,
        'index':len(blockchain),
        'transaction': open_transactions
    }
    blockchain.append(block)

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
    print("4. Quit")
    print("5. Hack the planet")
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        add_transaction(recipient, amount=amount)
        print(open_transactions)
    elif user_choice == '2':
        block_mine()
    elif user_choice == '3':
        print_blockchain()
    elif user_choice == '4':
        break
    elif user_choice == '5':
        if len(blockchain) > 0:
            blockchain[0] = {
                'previous_block_hash':'',
                'index':0,
                'transaction': {'sender': 'Sai', 'receiver': 'Max', 'amount':100}
            }
    else:
        print("Invalid choice")
    if not validate_blockchain():
        print('Invalid Chain!!!')
        break

