from tornado import web,websocket
import json

clients = []
names=[]
clientNames={}
class WSHandler(websocket.WebSocketHandler):
	def open(self):
		self.name="Anonymous"+str(id(self))
		self.to="all"
		clients.append(self)
		global clientNames
		clientNames={"name":"userNames","names":[]}
		for c in clients:
			clientNames["names"].append(c.name)
		for c in clients:
			c.write_message(json.dumps(clientNames))

	def on_message(self,message):
		if(message.startswith("name :")):
			self.name=message[6:]
			clientNames["names"]=[]
			for c in clients:
				clientNames["names"].append(c.name)
			for c in clients:
				c.write_message(json.dumps(clientNames))

		else:
			msg={"message":message}
			for c in clients:
				c.write_message(json.dumps(msg))

	def on_close(self):
		clients.remove(self)
		clientNames["names"]=[]
		for c in clients:
			clientNames["names"].append(c.name)
			c.write_message(json.dumps(clientNames))
		self.close()


class chatGroup(web.RequestHandler):
	def get(self):
		self.render("templates/chat.html")