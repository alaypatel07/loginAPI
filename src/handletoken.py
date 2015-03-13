__author__ = 'alay'

import redis
import json

# ttl: Time to Live in number of days
ttl = 1


class HandleToken():
    def __init__(self, token, username=None, rights=None):
        self.token = token
        self.username = username
        self.rights = rights
        self.data = json.dumps(dict(username=self.username, rights=self.rights))

    def set_token(self):
        db = redis.StrictRedis()
        return db.setex(self.token, ttl * 24 * 60 * 60, self.data)

    def exists(self):
        db = redis.StrictRedis()
        return db.exists(self.token)

    def del_token(self):
        db = redis.StrictRedis()
        return db.delete(self.token)

    def get_data(self):
        db = redis.StrictRedis()
        if self.exists():
            return db.get(self.token)