__author__ = 'alay'

from tornado.web import RequestHandler
from src import handledoc
from src.handletoken import HandleToken
from src import handler
import datetime
import traceback
import json


def get_data(url, token_handler):
    url = url.lstrip('/').rstrip('/')
    slugs = url.split('/')
    slugs.remove('data')
    token_handler.get_data()
    users = dict()
    users['username'] = token_handler.data['username']
    doc = handledoc.HandleDoc(users, "auth_user")
    if doc.exists() is not None:
        data = doc.doc
    if doc.exists():
        for each_slug in slugs:
            try:
                data = data[each_slug]
            except KeyError as key_error:
                return None
            except TypeError as type_error:
                return None
    return data



class DataHandler(handler.LoginRequestHandler):
    def post(self, *args, **kwargs):
        user = dict()
        request = self.request.uri
        token = self.get_argument('token')
        token_handler = HandleToken(token)
        if token_handler.exists():
            data = get_data(request, token_handler)
            del token_handler
            if data is None:
                self.send_error(404)
            else:
                self.message = data
                self.send_error(200)
        else:
            del token_handler
            self.send_error(403)