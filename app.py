from kivy.app import App
from kivy.uix.widget import Widget
import requests
import json


url = "https://api.henrikdev.xyz/valorant/v1/mmr/na/"



class ValorantApp(Widget):
    pass

class ValorantApp(App):
    def build(self):
        return ValorantApp()

if __name__ == '__app__':
    ValorantApp().run()


def registerAccount(name, tag):
    urlAc = url+name+'/'+tag
    x = requests.get(urlAc)
    getRank(x.text)

def getRank(playerData):
    y = json.loads(playerData)
    print(y["data"]["currenttierpatched"])





registerAccount("Comolly", "404")



