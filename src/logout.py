__author__ = 'alay'

from tornado.web import RequestHandler
from src import handledoc
import traceback


class LogoutHandler(handledoc.LoginRequestHandler):
    def post(self, *args, **kwargs):
        user = dict()
        token = self.get_argument('token')
        user['token'] = token
        user_doc = handledoc.HandleDoc(user)
        flag = user_doc.exists('logged_in_users')
        if flag is None:
            handledoc.failure_msg['error'] = 'tokenDoesntExist'
            self.send_error(404)
        else:
            doc_id = flag['id']
            user_doc.db.delete(doc_id)
            self.send_error(200)