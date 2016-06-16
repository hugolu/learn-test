import pymysql.cursors
from pymysql.cursors import Cursor

cnx = pymysql.connect(user='root', password='000000', host='127.0.0.1', db='test')
cursor = cnx.cursor()

def login_check(username, password):
    query = "SELECT password FROM account WHERE username='%s'" % username
    cursor.execute(query)
    row = cursor.fetchone()
    if row is not None:
        (pw,) = row
        return "successful" if pw == password else "failed"
    else:
        return "failed"

import unittest
from unittest.mock import Mock, patch
class TestAccount(unittest.TestCase):

    def setUp(self):
        def execute(_, query):
            if query == "SELECT password FROM account WHERE username='abcdef'":
                self.password = ("123456",)
            else:
                self.password = None
        def fetchone(_):
            return self.password
        self.execute = execute
        self.fetchone = fetchone

    def test_login_with_correct_username_password2(self):
        with patch('pymysql.cursors.Cursor.execute', self.execute):
            with patch('pymysql.cursors.Cursor.fetchone', self.fetchone):
                self.assertEqual(login_check("abcdef", "123456"), "successful")

    def test_login_with_invalid_username(self):
        with patch('pymysql.cursors.Cursor.execute', self.execute):
            with patch('pymysql.cursors.Cursor.fetchone', self.fetchone):
                self.assertEqual(login_check("ABCEDF", "123456"), "failed")

    def test_login_with_invalid_password(self):
        with patch('pymysql.cursors.Cursor.execute', self.execute):
            with patch('pymysql.cursors.Cursor.fetchone', self.fetchone):
                self.assertEqual(login_check("abcedf", "000000"), "failed")
