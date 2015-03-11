__author__ = 'alay'


from tornado.web import RequestHandler
from src import handledoc
import traceback


class RegisterHandler(RequestHandler):
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

    def get(self, *args, **kwargs):
        self.render('/home/alay/Documents/Projects/rajadhirajapi/templetes/register.html')

    def post(self, *args, **kwargs):
        user = dict()
        query = dict()
        user['first_name'] = self.get_argument('first_name')
        user['last_name'] = self.get_argument('last_name')
        user['email_id'] = self.get_argument('email_id')
        user['username'] = self.get_argument('username')
        user['password'] = self.get_argument('password')
        query['username'] = user['username']
        user_data = handledoc.HandleDoc(query)
        doc = user_data.exists("auth_user")
        if doc is None:
            user_data.insert_doc("auth_user", user)
            self.send_error(200)
        else:
            self.send_error(409)