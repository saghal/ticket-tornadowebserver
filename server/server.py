import os.path
import torndb
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os
from binascii import hexlify
import tornado.web
from tornado.options import define, options


define("port", default=1104, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="database host")
define("mysql_database", default="tickets", help="database name")
define("mysql_user", default="x", help="database user")
define("mysql_password", default="y", help="database password")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/signup", signup),
            (r".*", defaulthandler),
        ]
        settings = dict()
        super(Application, self).__init__(handlers, **settings)
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class signup(BaseHandler):
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        rool = self.get_argument('rool')
        api_token = str(hexlify(os.urandom(16)))
        user_id = self.db.execute("INSERT INTO users (username, password, rool,apitoken) "
                                 "values (%s,%s,%s,%s) "
                                 , username,password, rool,api_token)

        output = {'username' : username,
                  'status': 'OK'}

        self.write(output)

class defaulthandler(BaseHandler):
    def get(self):
        user = self.db.get("SELECT * from users where username = 'mohammadsgh'")
        self.write(user)

def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()