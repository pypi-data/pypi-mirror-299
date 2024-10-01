from typing import List

from src.components.IComponent import IComponent

from dash import html



class MenuComponent(IComponent):
    def __init__(self,componentOnRoute:List[IComponent]):
        self.components = componentOnRoute
        self.menu = None

    def build(self):
        self._setStyle()
        self._setTemplate()
        return self.menu

    def _setStyle(self):
        return "menu"

    def _setTemplate(self):
        self.menu = html.Div(
                    className=self._setStyle(),
                    children=(
                        html.Div(
                            className="card-button-menu",
                            children= [ component.build() for component in self.components]
                        ))
                )

    def getID(self) ->str:
        return self.id



