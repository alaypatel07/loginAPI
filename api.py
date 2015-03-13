__author__ = 'alay'

from tornado.web import Application
from tornado.web import RequestHandler
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import options, define
from src import login
from src import register
from src import data
from src import logout
from src.handler import LoginRequestHandler

define("port", default=8000, help="give the Port number for the server to run on", type=int)


class IndexHandler(LoginRequestHandler):
    def get(self, *args, **kwargs):
        self.render(self.root + '/templetes/index.html')
    

if __name__ == "__main__":
    api = Application(handlers=[
        (r'/', IndexHandler),
        (r'/logout', logout.LogoutHandler),
        (r'/login', login.LoginHandler),
        (r'/data(.*)', data.DataHandler),
        (r'/register', register.RegisterHandler)
    ])
    server = HTTPServer(api)
    server.listen(options.port)
    IOLoop.instance().start()