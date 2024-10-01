from src.components.IComponent import IComponent

from dash import html



class TextButtonComponent(IComponent):
    def __init__(self,id,title):
        self.id = id
        self.title = title
        self.textButton = None

    def build(self):
        self._setStyle()
        self._setTemplate()
        return self.textButton

    def _setStyle(self):
        return "text-btn-custom"

    def _setTemplate(self):
        self.textButton = html.P(children= self.title,
                                  id=self.id,
                                  className=self._setStyle(),
                                 )

    def getID(self) ->str:
        return self.id



