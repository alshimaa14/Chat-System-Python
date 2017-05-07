import tornado.web
import tornado.ioloop
import Users
import Group
import ChatHandler

application = tornado.web.Application([
    (r"/", Group.ShowGroups),
    (r"/addGroup", Group.InsertGroup),
    (r"/delGroup", Group.DeleteGroup),
    (r"/login",Users.Login),
    (r"/logout",Users.Logout),
    (r"/create" ,Users.SignUp),
    (r"/delFriend", Users.DeleteFriend),
    (r"/addFriend", Users.AddFriend),
    (r"/updateUser", Users.UpdateData),
    (r"/chat",ChatHandler.chatGroup),
    (r"/ws", ChatHandler.WSHandler)
],static_path='scripts',debug=True,cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=")

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
