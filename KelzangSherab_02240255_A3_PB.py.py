import unittest
from KelzangSherab_02240255_A3_PA import BankAccount, InvalidAmountError, InsufficientFundsError 

class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.account1 = BankAccount("Dechen", 1000)  # Bhutanese name
        self.account2 = BankAccount("Dorji", 500)

    def test_initial_balance(self):
        self.assertEqual(self.account1.balance, 1000)
        self.assertEqual(self.account2.balance, 500)

    def test_deposit(self):
        self.account1.deposit(200)
        self.assertEqual(self.account1.balance, 1200)
        with self.assertRaises(InvalidAmountError):
            self.account1.deposit(-100)
        with self.assertRaises(InvalidAmountError):
            self.account1.deposit(0)

    def test_withdraw(self):
        self.account1.withdraw(200)
        self.assertEqual(self.account1.balance, 800)
        with self.assertRaises(InsufficientFundsError):
            self.account1.withdraw(2000)
        with self.assertRaises(InvalidAmountError):
            self.account1.withdraw(-100)
        with self.assertRaises(InvalidAmountError):
            self.account1.withdraw(0)

    def test_transfer(self):
        self.account1.transfer(300, self.account2)
        self.assertEqual(self.account1.balance, 700)
        self.assertEqual(self.account2.balance, 800)
        with self.assertRaises(InsufficientFundsError):
            self.account1.transfer(2000, self.account2)
        with self.assertRaises(InvalidAmountError):
            self.account1.transfer(-100, self.account2)
        with self.assertRaises(InvalidAmountError):
            self.account1.transfer(0, self.account2)
        with self.assertRaises(InvalidAmountError):
            self.account1.transfer(100, self.account1)

    def test_mobile_topup(self):
        self.account1.mobile_topup(100, "17765367")  # B-Mobile number
        self.assertEqual(self.account1.balance, 900)
        with self.assertRaises(InsufficientFundsError):
            self.account1.mobile_topup(2000, "17765367")
        with self.assertRaises(InvalidAmountError):
            self.account1.mobile_topup(-100, "17765367")
        with self.assertRaises(InvalidAmountError):
            self.account1.mobile_topup(0, "17765367")

    def test_transaction_history(self):
        self.account1.deposit(200)
        self.account1.withdraw(100)
        self.account1.transfer(50, self.account2)
        self.account1.mobile_topup(25, "17765367")
        transactions = self.account1.get_transactions()
        self.assertEqual(len(transactions), 4)
        self.assertIn("Deposited Nu.200", transactions)
        self.assertIn("Withdrew Nu.100", transactions)
        self.assertIn("Sent Nu.50 to Dorji", transactions)
        self.assertIn("Mobile top-up Nu.25 to 17765367", transactions)

class TestProcessUserInput(unittest.TestCase):
    def setUp(self):
        self.accounts = {
            "Dechen": BankAccount("Dechen", 1000),
            "Dorji": BankAccount("Dorji", 500)
        }
        self.current_account = None

    def test_create_account(self):
        from kelzangSherab_02240255_A3_PA import processUserInput 
        accounts, _ = processUserInput('1', {}, None)
        self.assertEqual(len(accounts), 1)

    def test_select_account(self):
        from kelzangSherab_02240255_A3_PA import processUserInput
        _, current_account = processUserInput('2', self.accounts, None)
        self.assertIsNotNone(current_account)

    def test_invalid_account(self):
        from kelzangSherab_02240255_A3_PA import processUserInput
        _, current_account = processUserInput('2', self.accounts, None)
        self.assertIsNone(current_account)

    def test_deposit_no_account(self):
        from kelzangSherab_02240255_A3_PA import processUserInput
        _, current_account = processUserInput('3', self.accounts, None)
        self.assertIsNone(current_account)

    def test_withdraw_no_account(self):
        from kelzangSherab_02240255_A3_PA import processUserInput
        _, current_account = processUserInput('4', self.accounts, None)
        self.assertIsNone(current_account)

    def test_transfer_no_account(self):
        from kelzangSherab_02240255_A3_PA import processUserInput
        _, current_account = processUserInput('5', self.accounts, None)
        self.assertIsNone(current_account)

    def test_topup_no_account(self):
        from kelzangSherab_02240255_A3_PA import processUserInput
        _, current_account = processUserInput('6', self.accounts, None)
        self.assertIsNone(current_account)

    def test_delete_no_account(self):
        from kelzangSherab_02240255_A3_PA import processUserInput
        _, current_account = processUserInput('7', self.accounts, None)
        self.assertIsNone(current_account)

    def test_view_no_account(self):
        from kelzangSherab_02240255_A3_PA import processUserInput
        _, current_account = processUserInput('8', self.accounts, None)
        self.assertIsNone(current_account)

    def test_invalid_choice(self):
        from kelzangSherab_02240255_A3_PA import processUserInput
        accounts, current_account = processUserInput('99', self.accounts, None)
        self.assertEqual(accounts, self.accounts)
        self.assertIsNone(current_account)

if __name__ == "__main__":
    unittest.main()