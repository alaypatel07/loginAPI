__author__ = 'alay'


from tornado.web import RequestHandler
from src import handledoc


class RegisterHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('../templates/register.html')

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
            self.write(handledoc.successful_msg)
        else:
            self.write(handledoc.failure_msg) #isAlreadyTaken: True,Error: