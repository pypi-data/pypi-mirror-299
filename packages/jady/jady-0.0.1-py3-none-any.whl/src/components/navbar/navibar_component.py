from src.components.IComponent import IComponent

from dash import html



class NavibarComponent(IComponent):
    def __init__(self,title):
        self.title = title
        self.navibar = None

    def build(self):
        self._setStyle()
        self._setTemplate()
        return self.navibar

    def _setStyle(self):
        return "header"

    def _setTemplate(self):
        self.navibar = html.Div(
                    className=self._setStyle(),
                    children=(
                        html.Img(
                            className="card-logo",
                            src=  "https://labcidades.com.br/wp-content/uploads/2024/04/LOGO-LABCIDADES-01.webp",
                            ),
                        html.P(
                            className="card-title",
                            children= self.title
                        ),
                    )
                )

    def getID(self) ->str:
        return self.id



