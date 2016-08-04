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
    
    def __init__(self,target,server,**kwargs):
        super(chatTab, self).__init__(**kwargs)
        self.chatView.bind(minimum_height=self.chatView.setter('height'))
        self.text = target
        self.c = None
        self.id = str(target+server)

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
        
        existingCon = next((i for i in self.cons if i.connection.server == server and i.connection.nickname == nick), None)
        try:
            if existingCon != None:
                for i in self.chatScrn.ids.UItabs.tab_list:
                    if str(i.id) == str(target+server):
                        break
                    elif str(i.id) == None:
                        continue
                    else:
                        existingCon.connection.join(target) 
                        ircTab = chatTab(target,server)        
                        ircTab.c = existingCon
                        self.chatScrn.ids.UItabs.add_widget(ircTab)
                        break           
            else:
                ircTab = chatTab(target,server)        
                con = IRCCat(target)
                con.connect(server, port, nick)
                self.cons.append(con)    
                ircTab.c = con
                self.chatScrn.ids.UItabs.add_widget(ircTab)
                Thread(target=con.start,args=()).start()
        except irc.client.ServerConnectionError as x:
            print(x)
            sys.exit(0)
        
    def on_stop(self):
        for i in self.cons:
            try:
                i.connection.disconnect(message="kIRC") #not sending quit msg?
            except:
                pass      
        sys.exit(0)
        
kIRC = IrcApp()
kIRC.run()
