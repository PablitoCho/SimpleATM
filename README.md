# SimpleATM

## ATM Flowchart
![Alt text](https://github.com/PablitoCho/SimpleATM/blob/main/images/Flowchart.PNG?raw=true "Flowchart")

## Inspiration
 1. ATM does not have any card and account information. Only Bank does.
 2. A bank API wouldn't give the ATM the PIN number, but it can tell you if the PIN number is correct or not. (API check_PIN)
 3. ATM cannot execute transactions, it just asks Bank to do that. (API execute_tx)
 4. ATM writes log for every transaction.
 5. Bank refresh its database(`bank.database`) after every successful transaction. It doen not if transactions fail.
 6. PIN number is encrypted(SHA256) and stored in database.

## Instruction
 1. Clone repository.
 2. Make sure that classes.py, RunATM.py and bank.database are at same directory.
 3. In CMD prompt, type 'python RunATM.py' and enter.
 4. Follow guidances the prompt gives you. :)

 (I just used python standard libraries so that no additional installation is necessary.)

## Guidance
 For your convenience, I added 4 cards information. See the table below.

| card no.   |      PIN    |
|----------|:-------------:|
| 1424-5678-9012 |  5678 |
| 5555-6666-7777-9999 | 2468 |
| 1002-2222-4444-5555 | 8888 |
| 1234-5678-9012 | 1234 |

If you want to add new card or delete existing card information, see notebook `Debug.ipynb`.

## Classes
 1. **Bank**: Simulate how bank works. It gives ATM necessary APIs. Json file `bank.database` acts like bank database. It is updated when card or account information changes.
 2. **Card, Account, Transaction**: Represent card, account, transaction respectively.
 3. No specific class representing ATM. The main script `RunATM.py` acts as the ATM role. 

## Running Example
![Alt text](https://github.com/PablitoCho/SimpleATM/blob/main/images/Running.png?raw=true "CMD Example")
