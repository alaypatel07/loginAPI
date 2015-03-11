__author__ = 'alay'

from tornado.web import RequestHandler
from src import handledoc
import datetime
import traceback

class DataHandler(RequestHandler):
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
            self.set_header('Content-Type', 'text/plain')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()
        else:
            self.finish('{"status":' + str(status_code) + '", message":' + self._reason + '"}')

    def post(self, *args, **kwargs):
        user = dict()
        token = self.get_argument('token')
        user['token'] = token
        user_doc = handledoc.HandleDoc(user)
        flag = user_doc.exists('logged_in_users')
        if flag is None:
            self.send_error(403)
        else:
            doc_id = flag['id']
            token_expiry = user_doc.doc['expiry']
            timestamp = datetime.datetime.timestamp(datetime.datetime.now())
            if float(token_expiry) > timestamp:
                self.send_error(200)
            else:
                handledoc.failure_msg['error'] = 'tokenExpired'
                self.send_error(403)