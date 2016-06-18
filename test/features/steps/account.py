import mysql.connector

cnx = mysql.connector.connect(user='root', password='000000', host='127.0.0.1', database='test')
cursor = cnx.cursor()

def account_insert(username, password):
    query = "INSERT INTO account (username, password) VALUES ('%s', '%s')" % (username, password)
    cursor.execute(query)
    cnx.commit()

def account_login(username, password):
    query = "SELECT id FROM account WHERE username='%s' AND password='%s'" % (username, password)
    cursor.execute(query)
    row = cursor.fetchone()
    return (row is not None)

def account_register(username, password):
    if len(username) < 6 or len(password) < 6:
        return False
    account_insert(username, password)
    return True

import unittest
from unittest.mock import Mock, patch
class TestAccount(unittest.TestCase):

    def setUp(self):
        self.result = None

    def test_account_insert(self):
        with patch('mysql.connector.cursor.MySQLCursor.execute') as mock_execute:
            with patch('mysql.connector.connection.MySQLConnection.commit') as mock_commit:
                account_insert('abcdef', '123456')

        mock_execute.assert_called_with("INSERT INTO account (username, password) VALUES ('abcdef', '123456')")
        mock_commit.assert_called_with()

    def test_login_with_correct_username_password(self):
        def mock_execute(_, query):
            self.result = ('1',) if query == "SELECT id FROM account WHERE username='abcdef' AND password='123456'" else None
        def mock_fetchone(_):
            return self.result

        with patch('mysql.connector.cursor.MySQLCursor.execute', mock_execute):
            with patch('mysql.connector.cursor.MySQLCursor.fetchone', mock_fetchone):
                self.assertTrue(account_login('abcdef', '123456'))

    def test_login_with_invalid_username(self):
        def mock_execute(_, query):
            self.result = ('1',) if query == "SELECT id FROM account WHERE username='abcdef' AND password='123456'" else None
        def mock_fetchone(_):
            return self.result

        with patch('mysql.connector.cursor.MySQLCursor.execute', mock_execute):
            with patch('mysql.connector.cursor.MySQLCursor.fetchone', mock_fetchone):
                self.assertFalse(account_login('abc', '123456'))

    def test_login_with_invalid_password(self):
        def mock_execute(_, query):
            self.result = ('1',) if query == "SELECT id FROM account WHERE username='abcdef' AND password='123456'" else None
        def mock_fetchone(_):
            return self.result

        with patch('mysql.connector.cursor.MySQLCursor.execute', mock_execute):
            with patch('mysql.connector.cursor.MySQLCursor.fetchone', mock_fetchone):
                self.assertFalse(account_login('abcdef', '123'))

    def test_register_with_valid_username_password(self):
        with patch('mysql.connector.cursor.MySQLCursor.execute') as mock_execute:
            with patch('mysql.connector.connection.MySQLConnection.commit') as mock_commit:
                self.assertTrue(account_register('abcdef', '123456'))

        self.assertTrue(mock_execute.called)
        self.assertTrue(mock_commit.called)

    def test_reigster_with_invalid_username(self):
        with patch('mysql.connector.cursor.MySQLCursor.execute') as mock_execute:
            with patch('mysql.connector.connection.MySQLConnection.commit') as mock_commit:
                self.assertFalse(account_register('abc', '123456'))

        self.assertFalse(mock_execute.called)
        self.assertFalse(mock_commit.called)

    def test_register_with_invalid_password(self):
        with patch('mysql.connector.cursor.MySQLCursor.execute') as mock_execute:
            with patch('mysql.connector.connection.MySQLConnection.commit') as mock_commit:
                self.assertFalse(account_register('abcdef', '123'))

        self.assertFalse(mock_execute.called)
        self.assertFalse(mock_commit.called)
