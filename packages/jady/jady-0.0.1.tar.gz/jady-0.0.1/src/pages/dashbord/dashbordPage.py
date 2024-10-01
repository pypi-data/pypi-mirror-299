from typing import List

from src.components.IComponent import IComponent
from src.components.menu.menu_component import MenuComponent
from src.components.navbar.navibar_component import NavibarComponent
from src.pages.iPage import IPage



from dash import html

class DashbordPage(IPage):
    def __init__(self,title:str,componentOnRoute:List[IComponent]):
        self.title = title
        self.dashbord = None
        self.components = componentOnRoute


    def build(self):
        self._setStyle()
        self._setTemplate()
        return self.dashbord
    def _setTemplate(self):
        self.dashbord = html.Div(
             id="dashbord",
             className=self._setStyle(),
             children= [
                NavibarComponent(title=self.title).build(),
                MenuComponent(self.components).build(),
                 html.Div(
                     id="main",
                     className="sec",
                 )
             ]
        )
    def _setStyle(self) ->str:
        return "dasboard-layout"

    def router(self):
        pass