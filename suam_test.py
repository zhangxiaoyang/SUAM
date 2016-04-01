#!/usr/env/bin python
# coding: utf-8

import unittest
import json
import sys

import suam

with open('users.json', 'r') as f:
    g_users = json.load(f)

class TestSUAM(unittest.TestCase):

    def test(self):
        for college in g_users:
            print 'Testing', college
            user = g_users[college]
            self.assertEqual(suam.auth(user['userid'], user['password'], college), 0)
            self.assertEqual(suam.auth('abc@abc.com', 'abc12345678', college), 1)
