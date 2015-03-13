__author__ = 'alay'

import redis

# ttl: Time to Live in number of days
ttl = 1

class HandleToken():
    def __init__(self, username, token, rights):
        self.token = token
        self.username = username
        self.rights = rights

    def setToken(self):
        db = redis.StrictRedis()
        return db.setex(self.token, ttl * 24 * 60 * 60)

    def exists(self):
        db = redis.StrictRedis()
        return db.exists(self.token)

    def delToken(self):
        db = redis.StrictRedis()
        return db.delete(self.token)