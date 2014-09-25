import scene
from data import namespace
from widgets import Widget

class Scene(scene.Scene):
    def do_setup(self, parent):
        self.parent = parent
    
    def draw(self):
        scene.background(*self.parent.settings.bg_color)
        for widget in self.parent.widgets:
            if widget.visible:
                widget.draw()
    
    def touch_began(self, touch):
        for widget in self.parent.widgets:
            if widget.enabled:
                widget._touch_began(touch)
    
    def touch_moved(self, touch):
        for widget in self.parent.widgets:
            if widget.enabled:
                widget._touch_moved(touch)
    
    def touch_ended(self, touch):
        for widget in self.parent.widgets:
            if widget.enabled:
                widget._touch_ended(touch)

class App():
    def __init__(self):
        self._setup()
    
    def _setup(self):
        self.scene = Scene()
        self.scene.do_setup(self)
        self.widgets = []
        self.bounds  = scene.Rect(0, 0, 100, 100)
        
        self.settings = namespace({
            "bg_color": (0, 0, 0)
            })
        
        self.setup()
    
    def setup(self):
        pass
    
    def add_widget(self, widget):
        assert 1#isinstance(widget, Widget) or issubclass(widget.__class__, Widget)
        self.widgets.append(widget)
    
    def run(self):
        scene.run(self.scene)
