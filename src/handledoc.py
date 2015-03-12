__author__ = 'alay'

import pycouchdb
from tornado.web import RequestHandler
import traceback


localhost = "http://admin:admin@127.0.0.1:5984"


class LoginRequestHandler(RequestHandler):
    def write_error(self, status_code, **kwargs):
        """Override to implement custom error pages.

        ``write_error`` may call `write`, `render`, `set_header`, etc
        to produce output as usual.

        If this error was caused by an uncaught exception (including
        HTTPError), an ``exc_info`` triple will be available as
        ``kwargs["exc_info"]``.  Note that this exception may not be
        the "current" exception for purposes of methods like
        ``sys.exc_info()`` or ``traceback.format_exc``.
        """
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header('Content-Type', 'application/json')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()
        else:
            self.set_header('Content-Type', 'application/json')
            self.finish('{"status":' + str(status_code) + '", message":' + self._reason + '"}')


class GetString(dict):
    def __init__(self, inp):
        self.input = inp
        self.key_list = []
        self.string = ''
        for key in self.input:
            self.string = self.string + "doc." + key + " == '" + inp[key] + "'" + ' && '


class HandleDoc():
    def __init__(self, inp):
        self.input = inp
        self.input_string = GetString(self.input).string[:-4]
        self.db_server = pycouchdb.Server(localhost)
        self.doc = {}

    def exists(self, db_name):
        self.db = self.db_server.database(db_name)
        map_function = 'function(doc){ if(' + self.input_string + ') {emit("True", null)}}'
        try:
            doc_id = list(self.db.temporary_query(map_function))[0]['id']
            self.doc = self.db.get(doc_id)
            return list(self.db.temporary_query(map_function))[0]
        except IndexError as err:
            return None

    def insert_doc(self, db_name, doc):
        self.doc = doc
        db = self.db_server.database(db_name)
        return db.save(self.doc)




if __name__ == "__main__":
    user = {"username":"alaypatel07", "password":"password"}
    user_doc = HandleDoc(user)
    temp = user_doc.exists('auth_user')
    print(user_doc.doc)
    # if  temp is None:
    #     a = user_doc.insert_doc('testdb', user)
    #     print(a)
    # else:
    #     print(temp)