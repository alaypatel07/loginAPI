__author__ = 'alay'

from tornado.web import RequestHandler
from src import handledoc
from src import hashit
from src import hashit
from src import handler
from src import handledoc
from src import handler
from src.handletoken import HandleToken
import traceback


class LoginHandler(handler.LoginRequestHandler):
    def get(self, *args, **kwargs):
        self.render(self.root + '/templetes/login.html')

    def post(self, *args, **kwargs):
        user = dict()
        user['username'] = self.get_argument('username')
        user['password'] = hashit.get_hash(self.get_argument('password'))
        doc = handledoc.HandleDoc(user, "auth_user")
        flag = doc.exists()
        if flag is None:
            self.send_error(404)
        else:
            token = hashit.get_hash_time(user['username'], user['password'])
            user['token'] = token[0]
            user['expiry'] = token[1]
            user['rights'] = 'admin'
            user.pop('password')

            token_handler = HandleToken(user['token'], user['username'], user['rights'])
            if token_handler.set_token():
                self.message = token_handler.token
                del token_handler
                self.send_error(200)
            else:
                del token_handler
                self.send_error(500)
