import pymysql.cursors

cnx = pymysql.Connect(user='root', password='000000', host='127.0.0.1', db='test')
cursor = cnx.cursor()

def account_insert(username, password):
    query = "SELECT username, password FROM account WHERE username='%s' AND password='%s'" % (username, password)
    cursor.execute(query)
    row = cursor.fetchone()
    if row is None:
        query = "INSERT INTO account (username, password) VALUES ('%s', '%s')" % (username, password)
        cursor.execute(query)
        cnx.commit()

def account_login(username, password):
    query = "SELECT password FROM account WHERE username='%s'" % username
    cursor.execute(query)
    row = cursor.fetchone()
    if row is not None:
        (pw,) = row
        return True if pw == password else False
    else:
        return False

def account_register(username, password):
    print(username, password)
    if len(str(username)) < 6 or len(str(password)) < 6:
        return False
    else:
        account_insert(username, password)
        return True

import unittest
class TestAccount(unittest.TestCase):

    def test_login_with_correct_username_password(self):
        self.assertEqual(account_login("abcdef", "123456"), True)

    def test_login_with_invalid_username(self):
        self.assertEqual(account_login("ABCEDF", "123456"), False)

    def test_login_with_invalid_password(self):
        self.assertEqual(account_login("abcedf", "000000"), False)
