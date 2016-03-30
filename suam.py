#!/usr/bin/env python
# coding: utf-8

import json
import requests
import sys

class SUAMError(Exception):
    pass

class LoginFailedError(SUAMError):

    def __init__(self, *args):
        self.message = args[0] if args else type(self).__name__
        self.code = 1

class CollegeNotFoundError(SUAMError):

    def __init__(self, *args):
        self.message = args[0] if args else type(self).__name__
        self.code = 2

class UnknownError(SUAMError):

    def __init__(self, *args):
        self.message = args[0] if args else type(self).__name__
        self.code = 3


class SUAM(object):

    def __init__(self, rule_file='rules.json'):
        with open(rule_file, 'r') as f:
            self.rules = json.load(f)

    def auth(self, userid, password, college):
        if college not in self.rules:
            raise CollegeNotFoundError()

        rule = self.rules[college]
        meta = rule['meta']
        data = rule['data']
        normalize = meta['normalize']
        keywords = meta['keywords']

        params = {
            normalize['userid']: userid,
            normalize['password']: password,
        }
        for k in data:
            params[k] = data[k]

        resp = requests.get(meta['url'], params=params)
        if keywords['succ'] in resp.text:
            return 
        if keywords['fail'] in resp.text:
            raise LoginFailedError()
        raise UnknownError()


g_suam = SUAM()
def auth(*args):
    try:
        g_suam.auth(*args)
    except SUAMError, e:
        return e.code
    except:
        return -1
    return 0
