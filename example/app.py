import os
import tornado.ioloop
import tornado.web
import tornado.escape
import sys
sys.path.append("..")
import session


from base import BaseHandler

class Application(tornado.web.Application):   
  def __init__(self):   
    settings = dict(   
      # 设定 cookie_secret, 用于 secure_cookie   
      cookie_secret = "e446976943b4e8442f099fed1f3fea28462d5832f483a0ed9a3d5d3859f==78d",   
      # 设定 session_secret 用于生成 session_id   
      session_secret = "3cdcb1f00803b6e78ab50b466a40b9977db396840c28307f428b25e2277f1bcc",   
      # memcached 地址   
      memcached_address = ["127.0.0.1:11211"],   
      # session 过期时间   
      session_timeout = 60,   
      template_path = os.path.join(os.path.dirname(__file__), "templates"),   
      static_path = os.path.join(os.path.dirname(__file__), "static"),   
      xsrf_cookies = True,   
      login_url = "/login",   
    )   
   
    handlers = [   
      (r"/", MainHandler),   
      (r"/login", LoginHandler)   
    ]   
   
    # 初始化父类 tornado.web.Application   
    tornado.web.Application.__init__(self, handlers, **settings)   
    # 初始化该类的 session_manager   
    self.session_manager = session.SessionManager(settings["session_secret"], settings["memcached_address"], settings["session_timeout"])  
        
        
class MainHandler(BaseHandler):
    def get(self):
	username = self.get_current_user()
	print username
        self.write("What's up, " + username + "?")

class LoginHandler(BaseHandler):
    def post(self):
        self.session["user_name"] = self.get_argument("name")
        self.session.save()
	self.write('save user_name to session')

if __name__ == "__main__":
    app = Application()
    app.listen("8080")
    print "start on port 8080..."
    tornado.ioloop.IOLoop.instance().start()
