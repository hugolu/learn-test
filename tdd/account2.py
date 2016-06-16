import pymysql.cursors

cnx = pymysql.Connect(user='root', password='000000', host='127.0.0.1', db='test')
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
class TestAccount(unittest.TestCase):

    def test_login_with_correct_username_password(self):
        self.assertEqual(login_check("abcdef", "123456"), "successful")

    def test_login_with_invalid_username(self):
        self.assertEqual(login_check("ABCEDF", "123456"), "failed")

    def test_login_with_invalid_password(self):
        self.assertEqual(login_check("abcedf", "000000"), "failed")
