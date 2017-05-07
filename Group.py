import tornado.ioloop
import tornado.web
from connectDB import _execute
from PIL import Image
from io import StringIO
import os, uuid

__UPLOADS__ = "scripts/images/"

class ShowGroups(tornado.web.RequestHandler):
    def get(self):
        # if not self.current_user:
        #     self.redirect("/login")
        #     self.write("you must login")
        #     print("not login")
        #     return

        # get all groups
        query=''' select * from 'group' '''
        res = _execute(query)
        resultat = []
        for i in res:
            resultat.append(i)
        groups=resultat

        # get user groups
        if(self.get_secure_cookie("user")):
            id = self.get_secure_cookie("user")
            user_id = int(id)
        else:
            user_id=""
        query = ''' select * from 'group' INNER JOIN user_groups ON 'group'.id = user_groups.group_id where user_groups.user_id = '%s' ''' % (user_id)
        res = _execute(query)
        # print(res)
        mygroups = []
        for i in res:
            mygroups.append(i)

        # get all users
        query = ''' select * from 'users' where id != '%s' and id not in (select friend_id from user_friends where user_id = '%s') ''' % (
        user_id, user_id)
        res = _execute(query)
        users = []
        for i in res:
            users.append(i)

        # get user friends
        query = ''' select * from 'users' INNER JOIN user_friends ON 'user_friends'.friend_id = users.id and user_friends.user_id='%s' ''' % (
        user_id)
        res = _execute(query)
        myFriends = []
        for i in res:
            myFriends.append(i)

        username = self.get_secure_cookie("name")

        #get super friend
        query = ''' select * from users order by friends_count desc limit 4 '''
        res = _execute(query)
        superFriend = []
        for i in res:
            superFriend.append(i)
        for j in superFriend:
            print(superFriend[2])

        #get public figure friend
        query = ''' select * from users  order by figure_count desc limit 4 '''
        res = _execute(query)
        publicFig = []
        for i in res:
            publicFig.append(i)

        # get public party friend
        query = ''' select * from users order by party_count desc limit 4 '''
        res = _execute(query)
        print("dsd")
        print(res)
        partyFriend = []
        for i in res:
            partyFriend.append(i)

        # get public chatty one
        query = ''' select * from users order by chatty_count desc limit 4 '''
        res = _execute(query)
        partyFriend = []
        for i in res:
            partyFriend.append(i)

        self.render('templates/index.html',groups=groups,mygroups=mygroups,users=users,myFriends=myFriends,
                    username=username,user_id=user_id,superFriend=superFriend,publicFig=publicFig,
                    partyFriend=partyFriend)

class InsertGroup(tornado.web.RequestHandler):
    def post(self):
        name = self.get_argument("name")
        picture = self.get_argument("group_pic")
        picture='home/anas'


        # fileinfo = self.request.files['group_pic'][0]
        # fname = fileinfo['filename']
        # extn = os.path.splitext(fname)[1]
        # picture = str(uuid.uuid4()) + extn
        # fh = open(__UPLOADS__ + picture, 'w')

        owner = int(self.get_secure_cookie("user"))
        query1 = ''' insert into 'group' (name , pictrue , owner_id) values (%s , %s, %i) ''' % (
            "'" + name + "'", "'" + picture + "'", owner);

        # add to user_group table
        query2=''' select last_insert_rowid() from 'group' '''
        group_id=_execute(query1,query2)
        group_id=group_id[0][0]
        # print (group_id)
        query=''' insert into user_groups (user_id, group_id) values (%i, %i) ''' % (owner,group_id);
        print(query)
        _execute(query)
        query2 = ''' update users set party_count = party_count+1 where name = ('%s') ''' % (name)
        _execute(query2)
        query3 = ''' update users set figure_count = party_count+1 where name = ('%s') ''' % (name)
        _execute(query3)

        self.redirect('/')

class DeleteGroup(tornado.web.RequestHandler):
    def post(self):
        name = self.get_argument("name")
        group_id=self.get_argument("group_id")
        query='''delete from 'group' where id = '%s' ''' % (group_id)
        _execute(query)
        query2 = ''' update users set party_count = party_count-1 where name = ('%s') ''' % (name)
        _execute(query2)
        query3 = ''' update users set figure_count = party_count-1 where name = ('%s') ''' % (name)
        _execute(query3)
        self.redirect('/')
