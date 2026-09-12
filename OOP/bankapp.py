# This code is meant to pracrice inheritane and class for a bank mini application

class Bank_Account:
    def __init__(self, account_number, account_holder, balance= 0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.__balance = balance
        
    #create a function to deposite into account
    def Deposit (self, amount):
        if amount > 0:
            self.__balance += amount
            return True
        return False

    #create a function to withdraw for the account
    def withdraw (self, amount):
        if 0 < amount <= self.__balance:
            self.__balance =  amount
            return True
        return False

    #create a function to collect balance from account
    def get_balance(self):
        return self.__balance



Account =Bank_Account(676925783, "OMALE", 1000000)

#initialise the function to deposit

Account.Deposit(500000)
print(Account.get_balance())

#initialise the function to withdraw
Account.withdraw(700000)
print(Account.get_balance())





