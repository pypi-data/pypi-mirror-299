# app.py
from dash import Dash
from src.components.textbutton.textbutton_component import TextButtonComponent
from src.pages.dashbord.dashbordPage import DashbordPage


app = Dash(__name__)

btn = [TextButtonComponent(id="text-btn-sobre", title="Sobre o projeto"),
       TextButtonComponent(id="text-btn-dashbord", title="dashbord"),
       TextButtonComponent(id="text-btn-contato", title="contatos")]

app.layout = DashbordPage(title="LAB CIDADES - CACHOEIRO DE ITAPEMIRIM",componentOnRoute=btn).build()

def main():
    app.run_server(debug=False)


main()
