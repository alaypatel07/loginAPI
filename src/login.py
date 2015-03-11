__author__ = 'alay'

from tornado.web import RequestHandler
from src import handledoc
from src import hashit


class LoginHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("/home/alay/Documents/Projects/rajadhirajapi/templetes/login.html")

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
            self.finish('{"status":' + str(status_code) + ', "token":' + str(self.token[0]) + '}')

    def post(self, *args, **kwargs):
        user = dict()
        user['username'] = self.get_argument('username')
        user['password'] = self.get_argument('password')
        doc = handledoc.HandleDoc(user)
        flag = doc.exists("auth_user")
        if flag is None:
            self.send_error(404)
        else:
            self.token = hashit.get_hash(user['username'], user['password'])
            user['token'] = self.token[0]
            user['expiry'] = self.token[1]
            user['ip'] = self.request.remote_ip
            user.pop('password')
            user_doc = handledoc.HandleDoc(user)
            doc = user_doc.insert_doc("logged_in_users", user)
            self.write_error(200)