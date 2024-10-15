#!/usr/bin/python3
"""create a user token to sign in """

import base64
from api.v1.auth.basic_auth import BasicAuth
from models.user import User

"""create a User"""
user_email = "Blockboy@gmail.com"
user_clear_pwd = "9472"

user = User()
user.email = user_email
user.password = user_clear_pwd
print("New user: {}: {}".format(user.id, user.email))
user.save()

basic_clear = "{}:{}".format(user_email, user_clear_pwd)
print("Basic Base64: {}".format(base64.b64encode(basic_clear.encode('utf-8')).decode("utf-8")))
