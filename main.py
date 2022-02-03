import kivy
kivy.require("2.0.0")
import kivymd
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.textfield import MDTextField
from kivy.uix.videoplayer import VideoPlayer
import requests
from bs4 import BeautifulSoup
import re
import base64
import json
import yarl
from Cryptodome.Cipher import AES


main_url = "https://www1.gogoanime.pe"


headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}

#screen1 coding
class Screen1(Screen):
    def __init__(self, **kwargs):
        super(Screen1,self).__init__(**kwargs)
        self.animes = []
        self.anime_links = []
        #layout designing
        layout = FloatLayout()
        toolbar = MDToolbar(title="Watch Anime")
        toolbar.pos_hint={"top":1}
        layout.add_widget(toolbar)
        self.anime_input = MDTextField(
            hint_text = "Enter anime name",
            halign = "center",
            size_hint = (0.8,1),
            pos_hint = {"center_x" : 0.5 , "center_y":0.7},
            font_size = 55
        
        
        )
        layout.add_widget(self.anime_input)
        btn = MDFillRoundFlatButton(
            text = "Search",
            pos_hint={"center_x":0.5,"center_y":0.6},
            
            on_release = self.screen_switch

        )

        layout.add_widget(btn)
        self.add_widget(layout)
  
    def screen_switch(self,args):
       
        name = self.anime_input.text
        if len(name) > 1:
            name = name.replace(" ","-")
        search_url = main_url + "//search.html?keyword="+name
        r = requests.get(search_url,headers=headers)
        src = r.content
        soup = BeautifulSoup(src,'lxml')
        hrefs = soup.find_all("p",attrs={'class':'name'})


        #get all the links
        for h in hrefs:
            tags = str(h)
            link = tags.split('/')[2].split('"')[0]
            self.anime_links.append(link)

        #for the names
        for href in hrefs:
            href = str(href)
            anime_name = re.sub('<[^>]*>', '', href)
            
            self.animes.append(str(anime_name))
        self.manager.get_screen("s2").list1 = list(self.animes)
        self.manager.get_screen("s2").list2 = list(self.anime_links)
        self.manager.current = 's2'
        self.manager.transition.direction = 'left'

class Screen2(Screen):
    def __init__(self, **kwargs):
        super(Screen2, self).__init__(**kwargs)
    def on_enter(self):
       

        myb = MDBoxLayout(padding = 50, orientation = 'vertical')
        mys = ScrollView()
        myl = MDList()

        myb.add_widget(mys)
        mys.add_widget(myl)
        
        for i in range(len(self.list1)):
            myl.add_widget(
                OneLineListItem(
                    text = str(i+1) + ". " + self.list1[i] 
                    )
                )
        #layout.add_widget(myb)
        self.add_widget(myb)
        layout = FloatLayout()
        self.anime_index_input=MDTextField(

            hint_text = "Enter Index",
            #halign = "center",
            size_hint = (0.8,1),
           
            font_size = 35
                   
        )
        layout.add_widget(self.anime_index_input)
        btn = MDFillRoundFlatButton(
            text = "Search",
           
            pos_hint={"center_x":0.85,"center_y":0.05},
            on_release = self.screen_switch

        )

        layout.add_widget(btn)
        self.add_widget(layout)
    def screen_switch(self, instance):
        i = int(self.anime_index_input.text)
        i = i - 1
        self.anime_name = self.list2[i]
        self.manager.get_screen("s3").list = list(self.anime_name)
        self.manager.current = 's3'
        self.manager.transition.direction = 'left'

class Screen3(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
    def on_enter(self):
        self.anime_name = ""
        for i in self.list:
            self.anime_name += i
        
        ep_url = main_url + "/category/"+self.anime_name
        k = requests.get(ep_url,headers=headers)
        src2 = k.content
        soup2 = BeautifulSoup(src2,'lxml')
        eps = soup2.find("a",attrs={'href':'#',"class":"active"}).text
        first_episode = eps.split("-")[0]
        first_episode = int(first_episode)+1
        try:
            last_episode = eps.split("-")[1]
            last_episode = int(last_episode)
        except:
            last_episode = 1
        layout = FloatLayout()
        toolbar = MDToolbar(title="Episodes")
        toolbar.pos_hint={"top":1}
        layout.add_widget(toolbar)
        self.episode_num = MDTextField(
            hint_text = "Enter Episode[" + str(first_episode)+"-"+str(last_episode)+"]",
            size_hint = (0.8,1),
            pos_hint = {"center_x" : 0.5 , "center_y":0.7},
            font_size = 55)
        layout.add_widget(self.episode_num)
        btn = MDFillRoundFlatButton(
            text = "Search",
            pos_hint={"center_x":0.5,"center_y":0.6},
            on_press = self.screen_switch)
        
        layout.add_widget(btn)


        self.add_widget(layout)
    def screen_switch(self,instance):
        ep = str(self.episode_num.text)
        link = main_url + "/"+self.anime_name+"-episode-"+ep
        m = requests.get(link,headers=headers)
        src3 = m.content
        soup3 = BeautifulSoup(src3,'lxml')
        href = soup3.find("li",attrs={'class':'dowloads'})
        l = href.find('a')
        id = l.get('href')
        #print(id)
        self.manager.get_screen("s4").list1 = list(id)
        self.manager.current = 's4'
        self.manager.transition.direction = 'left'

class Screen4(Screen):
    
    def __init__(self, **kw):
        super().__init__(**kw)

    
    def on_enter(self):
        id = ""
       
        for i in self.list1:
            id += i
        

        download_url = id
        parsed_url = yarl.URL(download_url)
        anime_id = parsed_url.query.get('id')
        ajax_url = "https://gogoplay.io/encrypt-ajax.php"
        s = b"257465385929383"b"96764662879833288"
        x = anime_id.replace('%3d',"=")
        length = 16-(len(x)%16)
        data = x + chr(length)*length
        encrypted_ajax = base64.b64encode(AES.new(s, AES.MODE_CBC, iv=b'4206913378008135').encrypt(data.encode()))
        c = requests.get(
            ajax_url,
            params={
                'id' : encrypted_ajax.decode(),
                'time' : '69420691337800813569'

            },
            headers={'x-requested-with':'XMLHttpRequest'}
        )
        j= json.loads(c.text)
    
        
        
        self.q = []
        self.link = []
      
        for i in range(4):
            try:
                l= j['source'][i]['file']
                self.link.append(l)
                quality = j['source'][i]['label']
                self.q.append(quality)
            except:
                pass 

            
        #design the screen
      
        myb = MDBoxLayout(padding = 50, orientation = 'vertical')
        mys = ScrollView()
        myl = MDList()
        myb.add_widget(mys)
        mys.add_widget(myl)
        for i in range(len(self.q)):
            myl.add_widget(
                OneLineListItem(
                    text = str(i+1) + ". " + str(self.q[i])
                )
            )
        self.add_widget(myb)

        #layout for user input
        layout = FloatLayout()

        self.quality_index_input=MDTextField(
            hint_text = "Enter Index",
            size_hint = (0.8,1),
            pos_hint={"center_x":0.5,"center_y":0.6},
            font_size = 55
        )
        layout.add_widget(self.quality_index_input)
        btn = MDFillRoundFlatButton(
            text ="Watch",
            font_size = 23,
            pos_hint = {"center_x":0.5,"center_y":0.5},
            on_release = self.screen_switch

        )
        layout.add_widget(btn)
        self.add_widget(layout)
    def screen_switch(self,instance):
        i = int(self.quality_index_input.text)
        i -= 1
        l=self.link[i]
        self.manager.get_screen('s5').list = list(l)
        self.manager.current = 's5'
        self.manager.transition.direction = 'up'


 
class Screen5(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
    def on_enter(self):
        url = ""
        for i in self.list:
            url += i
        
  
        player = VideoPlayer(
            source = url,
            state = "play",
            options = {'allow_stretch': True,'eos':'stop'}
        )
        self.add_widget(player)

    

        
class myapp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = "DeepPurple"
        self.sm = ScreenManager()
        self.sm.add_widget(Screen1(name= "s1"))
 
        self.sm.add_widget(Screen2(name = 's2'))
        self.sm.add_widget(Screen3(name = "s3"))
        self.sm.add_widget(Screen4(name = "s4"))
        self.sm.add_widget(Screen5(name = "s5"))
        return self.sm


if __name__ =="__main__":
    app = myapp()
    app.run()
