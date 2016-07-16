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
    
    def __init__(self,title,address,**kwargs):
        super(chatTab, self).__init__(**kwargs)
        self.chatView.bind(minimum_height=self.chatView.setter('height'))
        self.text = title
        self.c = None
        self.id = str(title+address)
        
    def triggerMsg(self):
        e = Thread(target=self.c.send_it,args=(self.text,self.ids.msgInp.text))
        e.start()

class IRCCat(irc.client.SimpleIRCClient):
    def __init__(self,target):
        irc.client.SimpleIRCClient.__init__(self)
        self.target = target

    def on_welcome(self, connection, event):
        if irc.client.is_channel(self.target):
            connection.join(self.target)
        else:
            pass #destroy tab

    def on_disconnect(self, connection, event):
        self.connection.quit("Using irc.client.py")

    def on_pubmsg(self, connection, event):
        msgBox = chatMsg()
        msgBox.ids.senderLbl.text = event.source
        #msgBox.ids.timeLbl
        msgBox.ids.msgLbl.text = event.arguments[0]
        for i in kIRC.chatScrn.ids.UItabs.tab_list:
            if i.id == str(event.target + connection.server):
                i.chatView.add_widget(msgBox)
                break
    
    def on_action(self, connection, event):
        msgBox = chatMsg()
        msgBox.ids.senderLbl.text = event.source
        #msgBox.ids.timeLbl
        msgBox.ids.msgLbl.text = event.arguments[0]
        msgBox.ids.msgLbl.italic = True
        
        iTabs = 0
        
        if irc.client.is_channel(event.target):
			for i in kIRC.chatScrn.ids.UItabs.tab_list:
				if i.id == str(event.target + connection.server):
					i.chatView.add_widget(msgBox)
					break
        
        elif kIRC.chatScrn.ids.UItabs.tab_list:
            for i in kIRC.chatScrn.ids.UItabs.tab_list:
                if i.id == str(irc.client.NickMask(event.source).nick + connection.server):
                    i.chatView.add_widget(msgBox)
                    break
                elif i < len(kIRC.chatScrn.ids.UItabs.tab_list):
                    iTabs += 1
                    print(iTabs)
                    continue
                else:
                    self.addTab(connection, event, msgBox)
                    break
        else:
            self.addTab(connection, event, msgBox)
    
    def on_privmsg(self, connection, event):
        msgBox = chatMsg()
        msgBox.ids.senderLbl.text = event.source
        #msgBox.ids.timeLbl
        msgBox.ids.msgLbl.text = event.arguments[0]
        
        iTabs = 0
        
        if kIRC.chatScrn.ids.UItabs.tab_list:
            for i in kIRC.chatScrn.ids.UItabs.tab_list:
                if i.id == str(irc.client.NickMask(event.source).nick + connection.server):
                    i.chatView.add_widget(msgBox)
                    break
                elif i < len(kIRC.chatScrn.ids.UItabs.tab_list):
                    iTabs += 1
                    print(iTabs)
                    continue
                else:
                    self.addTab(connection, event, msgBox)
                    break
        else:
            addTab(connection, event)

    def addTab(self, connection, event, obj):
        self.connection.join(event.target) 
        ircTab = chatTab(irc.client.NickMask(event.source).nick,connection.server)        
        ircTab.c = self
        ircTab.chatView.add_widget(obj)
        kIRC.chatScrn.ids.UItabs.add_widget(ircTab)


    def send_it(self,recep,msg):
        while 1:
            if msg == '':
                break
            else:
                self.connection.privmsg(recep, msg)
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
                        nets.connection.join(target) 
                        ircTab = chatTab(target,server)        
                        ircTab.c = nets
                        print(str(target+server))
                        for tabs in self.chatScrn.ids.UItabs.tab_list:
                            if tabs.id == str(target+server):
                                pass
                            else:
                                self.chatScrn.ids.UItabs.add_widget(ircTab)
                                print(tabs.id)
                                break
                        break
                    elif nets < len(self.cons):
                        iCons += 1
                        print(iCons)
                        continue
                    else:
                        ircTab = chatTab(target,server)
                        con = IRCCat(target)
                        con.connect(server, port, nick)
                        self.cons.append(con)    
                        print(self.cons)    
                        ircTab.c = con
                        self.chatScrn.ids.UItabs.add_widget(ircTab)
                        Thread(target=con.start,args=()).start()
                        break
            else:
                ircTab = chatTab(target,server)        
                con = IRCCat(target)
                con.connect(server, port, nick)
                self.cons.append(con)    
                print(self.cons)    
                ircTab.c = con
                self.chatScrn.ids.UItabs.add_widget(ircTab)
                Thread(target=con.start,args=()).start()                        
        except irc.client.ServerConnectionError as x:
            print(x)
            sys.exit(0)
        
        def on_close(self):
            for i in self.cons:
                i.connection.quit("kIRC - look for me on github.")      

        
kIRC = IrcApp()
kIRC.run()
