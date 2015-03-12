__author__ = 'alay'

import hashlib
import datetime

#token life in Days
token_life = 1


def get_hash_time(username, password):
    time = datetime.datetime.timestamp(datetime.datetime.now())
    expiry_time = time + (token_life * 24 * 60 * 60)
    data = username + password + str(expiry_time)
    byte_data = data.encode('utf-8')
    hash = hashlib.md5(byte_data)
    hex_hash = hash.hexdigest()
    return [str(hex_hash), str(expiry_time)]

def get_hash(string):
    data = string.encode('utf-8')
    hash_obj = hashlib.md5(data)
    return hash_obj.hexdigest()


def compare_hash(hash1, hash2):
    if hash1 == hash2:
        return True
    else:
        return False

