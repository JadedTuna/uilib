from scene import *
from data import namespace
from PIL import Image as PILImage

__all__ = [
    "Widget",
    "Label",
    "Image",
    "Button",
    "ScrolledPanel"
]

class Widget(object):
    def __init__(self, parent=None, pos=(0, 0), size=(0, 0)):
        pos  = Point(*pos)
        size = Size(*size)
        if parent:
            pos.x += parent.bounds.x
            pos.y += parent.bounds.y
        
        self.widgets = []
        self.enabled = True
        self.visible = True
        self.bounds  = Rect(pos.x, pos.y, *size)
        self.parent  = None
    
    def add_widget(self, widget):
        assert isinstance(widget, Widget)
        self.widgets.append(widget)
    
    def _touch_began(self, touch):
        if not touch.location in self.bounds: return
        self.touch_began(touch)
        for widget in self.widgets:
            widget._touch_began(touch)
    
    def _touch_moved(self, touch):
        self.touch_moved(touch)
        for widget in self.widgets:
            widget._touch_moved(touch)
    
    def _touch_ended(self, touch):
        self.touch_ended(touch)
        for widget in self.widgets:
            widget._touch_ended(touch)
    
    def touch_began(self, touch):
        pass
    
    def touch_moved(self, touch):
        pass
    
    def touch_ended(self, touch):
        pass
    
    def getpos(self):
        return Point(self.bounds.x, self.bounds.y)
    
    def setpos(self, pos):
        self.bounds.x, self.bounds.y = pos
    
    def move(self, pos):
        self.bounds.x += pos[0]
        self.bounds.y += pos[1]
    
    def getsize(self):
        return Size(self.bounds.w, self.bounds.h)
    
    def setsize(self, size):
        self.bounds.w, self.bounds.h = size
    
    def getrealbounds(self):
        if not self.parent: return self.bounds
        x, y, w, h = self.bounds
        px, py, pw, ph = self.parent.bounds
        pwe = px + pw
        phe = py + ph
        
        if x + w > pwe:
            w = pwe - x
        if y + h > pwh:
            h = phe - y
        return Rect(x, y, w, h)
    
    def draw(self):
        for widget in self.widgets:
            widget.draw()


class Image(Widget):
    def __init__(self,
                 parent,
                 pilimage,
                 pos=(0, 0),
                 size=(0, 0)):
        Widget.__init__(self, parent, pos, size)
        assert isinstance(pilimage, PILImage.Image)
        self.setsize(pilimage.size)
        self.name = load_pil_image(pilimage)
    
    def draw(self):
        x, y, w, h = self.getrealbounds()
        image(self.name, x, y, w, h)


class Label(Widget):
    def __init__(self,
                 parent,
                 text,
                 font=("Courier", 12.),
                 color=(0, 0, 0),
                 pos=(0, 0),
                 size=(0, 0)):
        Widget.__init__(self, parent, pos, size)
        #tint(*color)
        self.name, size = render_text(text, *font)
        print self.name, size
        self.setsize(size)
        self.font  = font
        self.color = color
    
    def draw(self):
        x, y = self.bounds.as_tuple()[:2]
        x -= self.getsize().w
        y -= self.getsize().h
        tint(*self.color)
        image(self.name, x, y)
        Widget.draw(self)

class Button(Widget):
    def __init__(self, parent, text, pos=(0, 0), size=(100, 100)):
        Widget.__init__(self, parent, pos, size)
        
        self.text = Label(self, text, ("Courier", 10))
        self.text.move([i/2. for i in self.getsize()])
        self.settings = namespace({
            "bg_color": [(0.7, 0.7, 0.7),
                         (0.3, 0.6, 0.8)],
            "br_color": [(0.6, 0.6, 0.6),
                         (0.6, 0.7, 0.8)],
            "border":   2,
        })
        
        self.pressed = False
        
        self.add_widget(self.text)
    
    def draw(self):
        bg = self.settings.bg_color[self.pressed]
        br = self.settings.br_color[self.pressed]
        
        border     = self.settings.border
        x, y, w, h = self.bounds
        fill(*br)
        rect(x, y, w, h)
        x += border
        y += border
        w -= border * 2
        h -= border * 2
        fill(*bg)
        rect(x, y, w, h)
        Widget.draw(self)
    
    def touch_began(self, touch):
        self.pressed = 1
    
    def touch_ended(self, touch):
        self.pressed = 0

class ScrolledPanel(Widget):
    pass
