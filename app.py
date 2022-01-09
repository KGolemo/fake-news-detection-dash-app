#!/usr/bin/python
# -*- coding: utf-8 -*-

import preprocessing_functions
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px

example = '''
Najnowsze dane z raportu brytyjskiej Agencji Bezpieczeństwa Zdrowia 
(UKHSA) jak i Public Health Scotland, instytucji nadzorujących szczepienia 
przeciwko COVID-19 pokazują, że stosunek umieralności z powodu koronawirusa z 
Wuhan jest, jak jedna osoba „niezaszczepiona” do prawie pięć osób „w pełni 
zaszczepionych”. Z podanych informacji widać, że zdecydowana większość 
zgłoszonych zgonów ​​ma miejsce po otrzymaniu zastrzyków. Te informacje są 
wyraźnie sprzeczne z podawanymi przez producentów szczepionek, o ich rzekomej 
ich skuteczności i 90% wskaźniku zapobiegania śmiertelności, jak i 
rozpowszechnianą propagandą przez media i rządy poszczególnych państw. W związku 
z zaistniałą sytuacją angielskie media The Exposé zadały pytanie: „Jeśli 
zastrzyk Covid ma być w 90% skuteczny w zapobieganiu śmierci, dlaczego 
„zaszczepieni” ludzie obecnie umierają w stosunku 4,8:1 do „nieszczepionych” 
osób?”

Wniosek – UKHSA kłamie publicznie twierdząc, że szczepionki ratują życie, co 
jest sprzeczne z tym, co mówią podawane przez nich dane. Kłamią również inne 
instytucje, media jak i rządy promujące ten specyfik. Korzystając z danych VSR 
(Vaccine Surveillance Report) zebranych przez okres trzech miesięcy, The Exposé 
odkrył, że nie tylko odporność ludzi po zaszczepieniu na wrażego chińskiego 
wirusa spadła, ale również wyjątkowo szybko zanika odporność, która rzekomo 
jest wytwarzana ludiom przez te zastrzyki.
'''

app = dash.Dash()   #initialising dash app

app.layout = html.Div([
    html.H1('Wklej tekst i sprawdź jego wiarygodność!'),
    html.Hr(),

    html.Div([
        dcc.Textarea(
            id='input_text',
            value=example,
            style={'width': '100%', 'height': 200}
        ),
        html.Br(),
        # html.Button('Lematyzuj:', id='lem_button'),
        # html.Div(id='lem_text'),

        html.Button('Weryfikuj', id='ver_button'),
        html.Table([
            html.Tr([html.Td(['Klasyfikator NB:']), html.Td(id='NB')]),
            html.Tr([html.Td(['Klasyfikator SVC:']), html.Td(id='SVC')]),
            html.Tr([html.Td(['Klasyfikator RF:']), html.Td(id='RF')])

        ], style={'font-size': 26})
    ]),

])


if __name__ == '__main__':
    app.run_server()

