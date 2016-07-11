#Kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from kivy.uix.tabbedpanel import TabbedPanel

#IRC
import irc.client
import sys
from threading import Thread

Builder.load_file("kvirc.kv")

class ChatScreen(Screen):
	chatView = ObjectProperty(None)
	
	def __init__(self,**kwargs):
		super(ChatScreen, self).__init__(**kwargs)
		self.chatView.bind(minimum_height=self.chatView.setter('height'))


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

    def send_it(self):
		while 1:
			line = self.gui.chatScrn.ids.msgInp.text
			if line == '':
				break
			self.connection.privmsg(self.target, line)
			break
       
class IrcApp(App):
	sm = ScreenManager()

	def build(self):
		self.chatScrn = ChatScreen()
		self.sm.add_widget(self.chatScrn)
		
		return self.sm

	def startChat(self):
		self.chatScrn.ids.chatView.clear_widgets()
		server = self.chatScrn.ids.serverInp.text
		try: 
			if port or port != '':
				port = int(self.chatScrn.ids.portInp.text)
		except:
			port = 6667

		nick = self.chatScrn.ids.nickInp.text
		target = self.chatScrn.ids.targetInp.text

		self.c = IRCCat(target,self)
		try:
			self.c.connect(server, port, nick)
		except irc.client.ServerConnectionError as x:
			print(x)
			sys.exit(0)
		self.ircProcess = Thread(target=self.c.start,args=())
		self.ircProcess.start()
		
	def triggerMsg(self):
		Thread(target=self.c.send_it,args=()).start()
			
IrcApp().run()
