# -*- coding: utf-8 -*- 
import sys
from classes import Bank, Transaction, pretty_print

BANK_DATABASE = 'bank.database'

def run():
    # Initiate bank object with database file
    bank = Bank(database_file=BANK_DATABASE)
    # Initiate atm object with transaction log file
    while True:
        cardNumber = input("\nInsert(Enter) Card Number(Enter 'exit' to exit): ")
        if cardNumber.lower() == 'exit':
                print("\nThanks you! Have a good day :)")
                exit()
        card_exists = bank.find_card(card_number=cardNumber)
        # Loop till id is valid
        while not card_exists:
            cardNumber = input("\nNo Such Card. Insert(Enter) Card Number Again: ")
            card_exists = bank.find_card(card_number=cardNumber)

        givenPIN = input("\nEnter PIN Number: ")
        PIN_match = bank.check_PIN(card_number=cardNumber, given=givenPIN)
        count = 3
        while not PIN_match:
            if count == 0:
                print('\n Exit ATM machine.(PIN number incorrect)')
                sys.exit()
            givenPIN = input(f"\nIncorrect PIN Number. Re-Enter PIN Number({count} times left):")
            PIN_match = bank.check_PIN(card_number=cardNumber, given=givenPIN)
            count -= 1

        # Iterating over account session
        while True:
            # Select Accounts
            _, card = bank.get_card(card_number=cardNumber)
            card_number = card['cardNumber']
            pretty_print(card)
            num_accounts = len(card['accounts'])
            try:
                account_selection = input("\nEnter index of Account(Enter 'exit' to cancel):")
                account_idx = int(account_selection)
            except ValueError:
                if account_selection.lower() == 'exit':
                    break
                else:
                    print("\nInvalid input :(")
                    exit()
            while account_idx not in range(1, num_accounts+1):
                account_idx = int(input("\nIncorrect Selection. Enter index of Account Again: "))
            account_number  = card['accounts'][account_idx-1]['accountNumber']
            current_balance = int(card['accounts'][account_idx-1]['balance'])
            # Select transaction
            print("\n [1] Deposit \t [2] Withdraw \t [3] Cancel ")
            selection = int(input("\nEnter your selection: "))
            
            # Deposit
            if selection == 1:
                op = 'deposit'
                amount = int(input("\nEnter amount to deposit: "))
                # create deposit transaction
                tx = Transaction(
                    operation=op,\
                    card_number=card_number,\
                    account_number=account_number ,\
                    amount=amount
                )
                result, balance = bank.execute_tx(tx = tx, PIN=givenPIN)
                tx.set_status(result)
                tx.write_log(before=current_balance, after=balance)
            # Withdraw
            elif selection == 2:
                op = 'withdraw'
                amount = int(input("\nEnter amount to withdraw: "))
                # create withdraw transaction
                tx = Transaction(
                    operation=op,\
                    card_number=card_number,\
                    account_number=account_number ,\
                    amount=amount
                )
                result, balance = bank.execute_tx(tx = tx, PIN=givenPIN)
                if result == 3:
                    print('\n Exceed withdrawal amount limit :(')
                tx.set_status(result)
                tx.write_log(before=current_balance, after=balance)
            # Exit
            elif selection == 3:
                print("\nCancel process.")
                break
            # Otherwise
            else:
                print("\nInvalid choice :(")
                exit()


if __name__ == '__main__':
    run()