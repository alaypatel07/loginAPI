__author__ = 'alay'

import hashlib
import datetime


token_life = 1 # in Days


def get_hash(username, password):
    username = username
    password = password
    time = datetime.datetime.timestamp(datetime.datetime.now())
    expiry_time = time + (token_life * 24 * 60 * 60)
    data = username + password + str(expiry_time)
    byte_data = data.encode('utf-8')
    hash = hashlib.md5(byte_data)
    hex_hash = hash.hexdigest()
    return [str(hex_hash), str(expiry_time)]


def compare_hash(hash1, hash2):
    if hash1 == hash2:
        return True
    else:
        return False

