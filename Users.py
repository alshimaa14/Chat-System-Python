import tornado.ioloop
import tornado.web
from connectDB import _execute

# Sign Up
class SignUp(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/signUp.html')

    def post(self):
        name = self.get_argument("name")
        password = self.get_argument("pass")

        select = ''' select name from users where name = '%s' ''' % (name);
        res = _execute(select)

        if len(res) == 0:
            query = ''' insert into users (name , password,party_count,chatty_count,friends_count,figure_count) values (%s , %s, 0, 0, 0, 0) ''' % ( "'" + name + "'", "'" + password + "'");
            print(query)
            _execute(query)
            self.redirect("/")
            # self.render('templates/index.html')

        else:
            self.write("Sorry, Duplicated name, please enter another name !")
            self.render('templates/signUp.html')

# Login
class Login(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/login.html')

    def post(self):
        name = self.get_argument("name")
        password = self.get_argument("pass")
        self.set_secure_cookie("name", name[1])

        query = ''' select * from users where name = '%s' and password = '%s' ''' % (name,password);
        res = _execute(query)
        print(res)

        if len(res) == 0:
            self.write("Incorrect Username or Password!!")
            self.render('templates/login.html')

        else:
            print(res[0][1])
            id=res[0][0]
            user_name=res[0][1]
            self.set_secure_cookie("user", str(id))
            self.set_secure_cookie("name", str(user_name))
            self.redirect("/")

#logout
class Logout(tornado.web.RequestHandler):
    def get(self):
        print(self.current_user)
        self.clear_cookie("name")
        self.clear_cookie("user")
        self.render('templates/login.html')

# add friend
class AddFriend(tornado.web.RequestHandler):
    def post(self):
        id = self.get_secure_cookie("user")
        user_id = int(id)
        friend = self.get_argument("friendval")
        query = '''insert into 'user_friends' values('%s','%s') ''' % (user_id,friend)
        _execute(query)
        query = '''insert into 'user_friends' values('%s','%s') ''' % (friend,user_id)
        _execute(query)
        query2 = ''' update users set friends_count = friends_count+1 where id = ('%s') ''' %(user_id)
        _execute(query2)
        query3 = ''' update users set friends_count = friends_count+1 where id = ('%s') ''' % (friend)
        _execute(query3)

        self.redirect('/')

#delete friend
class DeleteFriend(tornado.web.RequestHandler):
    def post(self):
        id = self.get_secure_cookie("user")
        user_id = int(id)
        friend = self.get_argument("friendval")
        friend_id=self.get_argument("friend_id")
        query='''delete from 'user_friends' where user_id='%s' and friend_id = '%s' ''' % (user_id,friend_id)
        _execute(query)
        query1 = '''delete from 'user_friends' where user_id='%s' and friend_id = '%s' ''' % (friend_id,user_id)
        _execute(query1)
        query2 = ''' update users set friends_count = friends_count-1 where id = ('%s') ''' % (user_id)
        _execute(query2)
        query3 = ''' update users set friends_count = friends_count-1 where id = ('%s') ''' % (friend)
        _execute(query3)
        self.redirect('/')

#update user data
class UpdateData(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/setting.html')
    def post(self):
        id = self.get_secure_cookie("user")
        user_id = int(id)
        username = self.get_secure_cookie("name")
        name = self.get_argument("name")
        password = self.get_argument("pass")
        repass = self.get_argument("repass")
        if(password != repass):
            self.write("don't match password")
            self.render('templates/setting.html')
            message = "don't match password"
        else:
            query = ''' update users set name= '%s' ,password= '%s' where id= %i ''' %(name,password,user_id)
            _execute(query)
            message = "Updated"
            self.write("updated")
            self.render('templates/setting.html', username=username)

