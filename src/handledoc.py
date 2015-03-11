__author__ = 'alay'

import pycouchdb
localhost = "http://admin:admin@127.0.0.1:5984"
successful_msg = {"Success": True}
failure_msg = {"Success": False}


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