__author__ = 'alay'

from tornado.web import RequestHandler
from src import handledoc
import datetime

class DataHandler(RequestHandler):
    def post(self, *args, **kwargs):
        user = dict()
        token = self.get_argument('token')
        user['token'] = token
        user_doc = handledoc.HandleDoc(user)
        flag = user_doc.exists('logged_in_users')
        if flag is None:
            self.write(handledoc.failure_msg)
        else:
            doc_id = flag['id']
            token_expiry = user_doc.doc['expiry']
            timestamp = datetime.datetime.timestamp(datetime.datetime.now())
            if float(token_expiry) > timestamp:
                self.write(handledoc.successful_msg)
            else:
                handledoc.failure_msg['error'] = 'tokenExpired'
                self.write(handledoc.failure_msg)