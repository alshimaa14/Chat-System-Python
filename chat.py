from tornado import web,ioloop,websocket
import json

class MainHandler(web.RequestHandler):
    def get(self):
        self.render("chat.html")

clients = {}
class ChatHandler(websocket.WebSocketHandler):
    def open(self):
        clients[id(self)] = self
        print("Connection Opened")

    def on_message(self,msg):
        dic={}
        dic['msg']=msg
        dic['number']=123
        data=json.dumps(dic)
        data1=json.loads(data)
        for c in clients.keys():
            clients[c].write_message(data)
            print(type(data),":",data[0])
            print(type(data1),":",data1['msg'])

    def on_close(self):
        del clients[id(self)]

app = web.Application([
		(r"/", MainHandler),
		(r'/chat',ChatHandler)
	],debug=True)

app.listen(8888)
ioloop.IOLoop.current().start()
