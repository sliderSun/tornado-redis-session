import tornado.web
import sys
sys.path.append("..")
import session


class BaseHandler(tornado.web.RequestHandler):   
	def __init__(self, *argc, **argkw):   
    		super(BaseHandler, self).__init__(*argc, **argkw)   
   		 # 定义 handler 的 session, 注意，根据 HTTP 特点，每次访问都会初始化一个 Session 实例哦，这对于你后面的理解很重要   
    		self.session = session.Session(self.application.session_manager, self)   
   
  	# 这是干嘛的？用于验证登录...请 google 关于 tornado.web.authenticated, 其实就是 tornado 提供的用户验证   
	def get_current_user(self):   
    		return self.session.get("user_name")  
