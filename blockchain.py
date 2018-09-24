# simple simulator of blcokchain using lists

blockchain = []

def get_last_blockchain_value():
        if len(blockchain) < 1:
            return [1]
        return blockchain[-1]

def add_value(transanction_amount):
    blockchain.append([get_last_blockchain_value(), transanction_amount])
    print(blockchain)
    print("transanction added")

def validate_blockchain():
    block_index = 0
    is_valid = True
    for block in blockchain:
        if block_index == 0:
            block_index += 1 
            continue
        elif block[0] == blockchain[block_index -1]:
            is_valid = True
        else:
            is_valid = False
            break
        block_index += 1
    return is_valid
    
def get_transanction_value():
    return float(input("Enter your transanction amount: "))

def print_blockchain():
    print("Printing blockchain")
    for block in blockchain:
        print(block)
    print("Done!")

def get_user_choice():
    return input('Your choice: ')
    
while True:
    print("\nPlease choose")
    print("1. Add a transanction value")
    print("2. Print blockchian")
    print("3. Quit")
    print("4. Hack the planet")
    user_choice = get_user_choice()
    if user_choice == '1':
        tr_amount = get_transanction_value()
        add_value(tr_amount)
    elif user_choice == '2':
        print_blockchain()
    elif user_choice == '3':
        break
    elif user_choice == '4':
        if len(blockchain) > 0:
            blockchain[0] = [2]
    else:
        print("Invalid choice")
    if not validate_blockchain():
        print('Invalid Chain!!!')
        break

