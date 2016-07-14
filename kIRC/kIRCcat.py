#Kivy
from kivy.app import App
from kivy.lang import Builder

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.label import Label


#IRC
import irc.client
import sys
from threading import Thread

Builder.load_file("kvirc.kv")

class ChatScreen(Screen):
	pass
 
class chatMsg(GridLayout):
	pass

class chatTab(TabbedPanelItem):
	chatView = ObjectProperty(None)
	
	def __init__(self,title,**kwargs):
		super(chatTab, self).__init__(**kwargs)
		self.chatView.bind(minimum_height=self.chatView.setter('height'))
		self.text = title
		self.c = None
		
	def triggerMsg(self):
		e = Thread(target=self.c.send_it,args=())
		e.start()

class IRCCat(irc.client.SimpleIRCClient):
	def __init__(self, target, gui):
		irc.client.SimpleIRCClient.__init__(self)
		self.target = target
		self.gui = gui

	def on_welcome(self, connection, event):
		if irc.client.is_channel(self.target):
			connection.join(self.target)
		else:
			pass

	def on_disconnect(self, connection, event):
		self.connection.quit("Using irc.client.py")

	def on_pubmsg(self, connection, event):
		msgBox = chatMsg()
		msgBox.ids.senderLbl.text = event.source
		#msgBox.ids.timeLbl
		msgBox.ids.msgLbl.text = event.arguments[0]
		self.gui.ids.chatView.add_widget(msgBox)
		print event
	
	def on_privmsg(self, connection, event):
		msgBox = chatMsg()
		msgBox.ids.senderLbl.text = event.source
		#msgBox.ids.timeLbl
		msgBox.ids.msgLbl.text = event.arguments[0]
		self.gui.ids.chatView.add_widget(msgBox)
		print event

	def send_it(self):
		while 1:
			line = self.gui.ids.msgInp.text
			if line == '':
				break
			self.connection.privmsg(self.target, line)
			break
	   
class IrcApp(App):
	sm = ScreenManager()
	cons = []
	def build(self):
		self.chatScrn = ChatScreen()
		self.sm.add_widget(self.chatScrn)
		return self.sm

	def startChat(self):
		server = self.chatScrn.ids.serverInp.text
		try: 
			if port != '':
				port = int(self.chatScrn.ids.portInp.text)
		except:
			port = 6667

		nick = self.chatScrn.ids.nickInp.text
		target = self.chatScrn.ids.targetInp.text
		
		iCons = 0
		try:
			if self.cons:
				for nets in self.cons:
					if nets.connection.server == server and nets.connection.nickname == nick:
						nets.connection.join(target) #need to join with an object that already has the con
						ircTab = chatTab(target)		
						ircTab.c = nets
						self.chatScrn.ids.UItabs.add_widget(ircTab)
						break
					elif nets < len(self.cons):
						iCons += 1
						print iCons
						continue
					else:
						ircTab = chatTab(target)
						con = IRCCat(target,ircTab)
						con.connect(server, port, nick)
						self.cons.append(con)	
						print self.cons	
						ircTab.c = con
						self.chatScrn.ids.UItabs.add_widget(ircTab)
						Thread(target=con.start,args=()).start()
						break
			else:
				ircTab = chatTab(target)		
				con = IRCCat(target,ircTab)
				con.connect(server, port, nick)
				self.cons.append(con)	
				print self.cons	
				ircTab.c = con
				self.chatScrn.ids.UItabs.add_widget(ircTab)
				Thread(target=con.start,args=()).start()						
		except irc.client.ServerConnectionError as x:
			print(x)
			sys.exit(0)		

		
IrcApp().run()
