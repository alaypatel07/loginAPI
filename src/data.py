__author__ = 'alay'

from tornado.web import RequestHandler
from src import handledoc
from src.handletoken import HandleToken
from src import handler
import datetime
import traceback


class DataHandler(handler.LoginRequestHandler):
    def post(self, *args, **kwargs):
        user = dict()
        token = self.get_argument('token')
        token_handler = HandleToken(token)
        if token_handler.exists():
            self.send_error(200)
        else:
            self.send_error(403)
        # user['token'] = token
        # user_doc = handledoc.HandleDoc(user)
        # flag = user_doc.exists('logged_in_users')
        # if flag is None:
        #     self.send_error(403)
        # else:
        #     doc_id = flag['id']
        #     token_expiry = user_doc.doc['expiry']
        #     timestamp = datetime.datetime.timestamp(datetime.datetime.now())
        #     if float(token_expiry) > timestamp:
        #         self.send_error(200)
        #     else:
        #         self.message = 'tokenExpired'
        #         self.send_error(408)