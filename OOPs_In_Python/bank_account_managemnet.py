class Account:
    bank_name = "National Bank"
    minimum_balance = 50
    total_accounts = 0

    def __init__(self, account_number, holder_name, balance):
        if not holder_name:
            raise ValueError("Account holder name cannot be empty.")
        if balance < 0:
            raise ValueError("Initial balance cannot be negative.")

        self._account_number = account_number
        self._holder_name = holder_name
        self._balance = balance
        Account.total_accounts += 1

    # ----- Instance Methods -----
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self._balance - amount < Account.minimum_balance:
            return "Withdrawal denied: Below minimum balance"
        self._balance -= amount
        return "Withdrawal successful"

    def get_balance(self):
        return self._balance

    def __str__(self):
        return f"{self._holder_name} ({self._account_number}) - Balance: ${self._balance:.2f}"

    # ----- Class Methods -----
    @classmethod
    def get_total_accounts(cls):
        return cls.total_accounts

    @classmethod
    def set_bank_name(cls, name):
        cls.bank_name = name

    @classmethod
    def set_minimum_balance(cls, amount):
        cls.minimum_balance = amount


# ---------- Savings Account ----------
class SavingsAccount(Account):
    def __init__(self, account_number, holder_name, balance, interest_rate):
        super().__init__(account_number, holder_name, balance)
        if interest_rate < 0:
            raise ValueError("Interest rate cannot be negative.")
        self._interest_rate = interest_rate  # annual interest in %

    def calculate_monthly_interest(self):
        interest = (self._balance * (self._interest_rate / 100)) / 12
        self._balance += interest
        return round(interest, 2)


# ---------- Checking Account ----------
class CheckingAccount(Account):
    def __init__(self, account_number, holder_name, balance, overdraft_limit):
        super().__init__(account_number, holder_name, balance)
        if overdraft_limit < 0:
            raise ValueError("Overdraft limit cannot be negative.")
        self._overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self._balance + self._overdraft_limit < amount:
            return "Withdrawal denied: Exceeds overdraft limit"
        self._balance -= amount
        return "Withdrawal successful"


# ---------- ✅ TEST CASES ----------
savings_account = SavingsAccount("SA001", "Alice Johnson", 1000, 2.5)
checking_account = CheckingAccount("CA001", "Bob Smith", 500, 200)

print(f"Savings Account: {savings_account}")
print(f"Checking Account: {checking_account}")

# Deposit and Withdrawal
print(f"Savings balance before: {savings_account.get_balance()}")
savings_account.deposit(500)
print(f"After depositing $500: {savings_account.get_balance()}")
withdrawal_result = savings_account.withdraw(200)
print(f"Withdrawal result: {withdrawal_result}")
print(f"Balance after withdrawal: {savings_account.get_balance()}")

# Overdraft Test
print(f"Checking balance: {checking_account.get_balance()}")
overdraft_result = checking_account.withdraw(600)
print(f"Overdraft withdrawal: {overdraft_result}")
print(f"Balance after overdraft: {checking_account.get_balance()}")

# Interest Calculation
interest_earned = savings_account.calculate_monthly_interest()
print(f"Monthly interest earned: {interest_earned}")

# Class Methods
print(f"Total accounts created: {Account.get_total_accounts()}")
print(f"Bank name: {Account.bank_name}")

Account.set_bank_name("New National Bank")
Account.set_minimum_balance(100)
print(f"Updated Bank name: {Account.bank_name}")

# Validation
try:
    invalid_account = SavingsAccount("SA002", "", -100, 1.5)
except ValueError as e:
    print(f"Validation error: {e}")
