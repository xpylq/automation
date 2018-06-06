#!/usr/bin/python3
class user:
    id = ''
    name = ''
    password = ''
    type = ''
    loginFlag = ''
    cookies = {}

    def __init__(self, id, name, password, type, loginFlag, cookies):
        self.id = id
        self.name = name
        self.password = password
        self.type = type
        self.loginFlag = loginFlag
        self.cookies = cookies


