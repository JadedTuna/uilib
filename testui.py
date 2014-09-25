import uilib
import sys
def reload_all(mod, name):
    reload(mod)
    for mod in sys.modules:
        if mod.startswith("{}".format(name)):
            print mod
            rmod = sys.modules[mod]
            if rmod:
                reload(rmod)

reload_all(uilib, "uilib")
from PIL import Image

class App(uilib.App):
    def setup(self):
        self.settings.bg_color = (0.9, 0.9, 0.9)
        button = uilib.Button(self,
                              "OK",
                              (250, 100),
                              (80, 35))
        label  = uilib.Label(self,
                             "Download completed!",
                             ("monofur", 20),
                             (0, 0, 0),
                             (200, 200))
        info   = uilib.Image(self,
                             Image.open("info.png"))
        
        self.add_widget(button)
        self.add_widget(label)
        #self.add_widget(info)

app = App()
app.run()
