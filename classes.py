# -*- coding: utf-8 -*- 
import uuid
import hashlib
import json

def find_index(ls, flt): # find index
    try:
        return [i for i,x in enumerate(ls) if flt(x)][0]
    except IndexError:
        return None # Not found

def find_element(ls, flt): # find element
    try:
        return list(filter(flt, ls))[0]
    except IndexError:
        return None # Not found

def pretty_print(card):
    print(f"\nCard Name : {card['cardName']}")
    print(f"Card Number : {card['cardName']}")
    row_format =" {:>3}{:>20}{:>30}{:>20}"
    print('\n * Accounts Info ' + '-'*58)
    print(row_format.format('idx', 'account name', 'account number', 'balance'))
    for i, account in enumerate(card['accounts']):
        print(row_format.format(i+1, account['accountName'], account['accountNumber'], account['balance']))


class Transaction(object):
    def __init__(self,  operation, card_number, account_number, amount, log_file = 'transactions.log'):
        self.id = str(uuid.uuid4())[:30]
        self.operation = operation # deposit, withdraw
        self.card_number = card_number
        self.account_number = account_number
        self.amount = amount
        self.status = None 
        self.log_file = log_file

    def set_status(self, result):
        self.status = result

    def write_log(self, before, after):
        result = "success" if self.status==0 else 'fail'
        log_line = '|'.join([self.id, self.card_number, self.account_number,\
            self.operation, str(before), str(after), result]) + '\n'
        with open(self.log_file, 'a+') as f:
            f.write(log_line)

class Account(object):
    def __init__(self, account_dict):
        self.name    = account_dict['accountName']
        self.number  = account_dict['accountNumber']
        self.balance = int(account_dict['balance'])
    
    def __repr__(self):
        return f"{self.name}({self.number}):{self.balance}"

    def to_dict(self):
        account_dict = {}
        account_dict['accountName']   = self.name
        account_dict['accountNumber'] = self.number
        account_dict['balance']       = self.balance
        return account_dict
    
    def get_balance(self):
        return self.balance

    def set_balance(self, balance):
        self.balance = balance

class Card(object):
    def __init__(self, card_dict):
        self.name = card_dict['cardName']
        self.number = card_dict['cardNumber']
        self.PIN = card_dict['pinNumber']
        self.accounts = []
        for account in card_dict['accounts']:
            self.accounts.append(Account(account))
    
    def get_account(self, account_number):
        flt = lambda x:x.number == account_number
        index = find_index(ls = self.accounts, flt = flt)
        account  = find_element(ls = self.accounts, flt = flt)
        return index, account
    
    def add_account(self, account_dict):
        new_account = Account(account_dict)
        self.accounts.append(new_account)
        
    def update_account(self, account_number, new_dict):
        assert account_number == new_dict['accountNumber']
        self.delete_account(account_number)
        self.add_account(new_dict)
        
    def delete_account(self, account_number):
        flt = lambda x:x.number == account_number
        index = find_index(ls = self.accounts, flt = flt)
        if index is not None:
            self.accounts.pop(index)

    def __repr__(self):
        return f"{self.name}({self.number}):{self.accounts}"
    
    def to_dict(self):
        card_dict = {}
        card_dict['cardName']   = self.name
        card_dict['cardNumber'] = self.number
        card_dict['pinNumber']  = self.PIN
        card_dict['accounts'] = []
        for account in self.accounts:
            card_dict['accounts'].append(account.to_dict())
        return card_dict

class Bank(object):
    def __init__(self, database_file):
        self.database_file = database_file
        try:
            with open(database_file) as json_file:
                self.database = json.load(json_file)
        except FileNotFoundError:
            raise Exception(f"[Error]Given database file {database_file} does not exist.")
        self.cards = self.database['card']
        
    def save_database(self):
        data = {}
        data['card'] = []
        for card in self.cards: # update latest information
            data['card'].append(card)
        with open(self.database_file, 'w') as outfile:
            json.dump(data, outfile)

    def check_PIN(self, card_number, given):
        # None : No card info found.
        # True or False : PIN match result
        card_number_str = str(card_number)
        flt = lambda x:x['cardNumber'].replace('-', '')==card_number_str.replace('-', '')
        card_dict = find_element(ls = self.cards, flt = flt)
        if card_dict is None: # Not reachable
            print(f"[Error]No such card with given number {card_number}")
            return None
        else:
            return card_dict['pinNumber'] == \
                    hashlib.sha256(str(given).encode()).hexdigest()
    
    def execute_tx(self, tx, PIN):
        if not self.check_PIN(tx.card_number, PIN):
            return -1 # authentification fails
        # return result, balance after transaction
        _, card_dict = self.get_card(tx.card_number)
        if card_dict is None:
            return 1, None # No card info. Not reachable?
        card = Card(card_dict)
        _, account = card.get_account(tx.account_number)
        if account is None:
            return 2, None # No account info.
        balance = account.get_balance()
        if tx.operation.lower() == 'deposit':
            new_balance = balance + tx.amount
        elif tx.operation.lower() == 'withdraw':
            new_balance = balance - tx.amount
            if new_balance < 0:
                return 3, balance # Tried to withdraw beyond avaliable
        account.set_balance(new_balance)
        new_account_dict = account.to_dict()
        card.update_account(tx.account_number, new_account_dict)
        new_card_dict = card.to_dict()
        self.update_card(card_dict, new_card_dict)
        return 0, new_balance

    def _printCardsList(self):
        for i, card_dict in enumerate(self.cards):
            card = Card(card_dict)
            print(f'[{i+1}] cardName {card.name} cardNumber {card.number}')

    def find_card(self, card_number):
        card_number_str = str(card_number)
        # Remove hyphen
        flt = lambda x : x['cardNumber'].replace('-', '') == card_number_str.replace('-', '')
        return find_index(ls = self.cards, flt = flt) is not None

    def get_card(self, card_number):
        card_number_str = str(card_number)
        # Remove hyphen
        flt = lambda x : x['cardNumber'].replace('-', '') == card_number_str.replace('-', '')
        index = find_index(ls = self.cards, flt = flt)
        card_dict = find_element(ls = self.cards, flt = flt)
        card_dict['accounts'] = sorted(card_dict['accounts'], key=lambda k: k['accountName']) 
        return index, card_dict
    
    def add_card(self, card_dict):
        accounts_ls = [account['accountNumber'] for account in card_dict['accounts']]
        if len(accounts_ls) != len(list(set(accounts_ls))):
            return 3
        for card in self.cards:
            if card_dict['cardNumber'] == card['cardNumber']:
                # Card number already exists. Transaction ends.
                return 1
            else:
                for account in card['accounts']:
                    if account['accountNumber'] in accounts_ls:
                         # Account Number already taken. Transaction ends.
                        return 2
        self.cards.append(card_dict)
        self.save_database()
        return 0

    def update_card(self, card_dict, new_dict):
        assert card_dict['cardNumber'] == new_dict['cardNumber']
        self.delete_card(card_dict['cardNumber'])
        result = self.add_card(new_dict)
        if result > 0:
            print(f"[Error]Failed to add card with number {card_dict['cardNumber']}")
        else:
            self.save_database()

    def delete_card(self, card_number):
        flt = lambda x : x['cardNumber'] == card_number
        index = find_index(ls = self.cards, flt = flt)
        if index is not None:
            self.cards.pop(index)
            self.save_database()
        else:
            print(f"[Error]No such card with given number {card_number}")
        
    def __del__(self):
        self.save_database()
