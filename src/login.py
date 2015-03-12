__author__ = 'alay'

from tornado.web import RequestHandler
from src import handledoc
from src import hashit
from src import hashit
from src import handler
from src import handledoc
from src import handler
import traceback


class LoginHandler(handler.LoginRequestHandler):
    def get(self, *args, **kwargs):
        self.render(self.root + '/templetes/login.html')


    def post(self, *args, **kwargs):
        user = dict()
        user['username'] = self.get_argument('username')
        user['password'] = hashit.get_hash(self.get_argument('password'))
        doc = handledoc.HandleDoc(user)
        flag = doc.exists("auth_user")
        if flag is None:
            self.send_error(404)
        else:
            self.token = hashit.get_hash_time(user['username'], user['password'])
            user['token'] = self.token[0]
            user['expiry'] = self.token[1]
            user['ip'] = self.request.remote_ip
            user.pop('password')
            user_doc = handledoc.HandleDoc(user)
            doc = user_doc.insert_doc("logged_in_users", user)
            self.message = str(self.token[0])
            self.send_error(200)
