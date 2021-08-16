import sqlite3
import unittest

class TestDB(TestCase):
    conn = None

    def make_connection(self):
        