from kivy.app import App
from kivy.uix.widget import Widget

class ValorantApp(Widget):
    pass

class ValorantApp(App):
    def build(self):
        return ValorantApp()

if __name__ == '__app__':
    ValorantApp().run()


