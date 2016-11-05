__author__ = 'alay'

from tornado.web import RequestHandler
from src import handledoc
from src import hashit


class LoginHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("../templates/login.html")

    def post(self, *args, **kwargs):
        user = dict()
        user['username'] = self.get_argument('username')
        user['password'] = self.get_argument('password')
        doc = handledoc.HandleDoc(user)
        flag = doc.exists("auth_user")
        if flag is None:
            self.write(handledoc.failure_msg)
        else:
            token = hashit.get_hash(user['username'], user['password'])
            user['token'] = token[0]
            user['expiry'] = token[1]
            user['ip'] = self.request.remote_ip
            user.pop('password')
            user_doc = handledoc.HandleDoc(user)
            doc = user_doc.insert_doc("logged_in_users", user)
            self.write('{"Success":"True", "token";"' + token[0] + '", "redirect":"/data", "expiry":"' + str(token[1]) + '"}')