#!/usr/bin/python
# -*- coding: utf-8 -*-

import preprocessing_functions
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
from joblib import load
import plotly.graph_objects as go
import plotly.express as px

example = '''Norwegia była do niedawna rajem nie tylko dla Polaków szukających godziwego zarobku, ale i oazą wolności w czasach 
kowidyzmu. Jednakże sataneria dobiera taktyki do mentalności konkretnego narodu. W związku z tym, że Norwedzy są 
posłuszni rządowi z natury, to ze szczepieniami nie było problemu. Ponad 70% Norwegów uwierzyło propagandzie. Jaki 
jest tego skutek? Teraz już nie mogą zganiać na antyszczepionkowców przy takim wskaźniku zakażeń. Jest to klęska idei 
budowania odporności produktem mRNA. Brawo Polonia w Norwegii. Polonia nie zadźgana. Grypa Hiszpanka wraca tym razem 
nazywana ponownie niesłusznie  bo wirusem z Wuhan. Podobnie jak 100 lat temu od dźgania umiera masa ludzi.
'''

app = dash.Dash()   #initialising dash app

colors = {
    'background': '#FAFAFA',
    'text': '#262626'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Wklej tekst i sprawdź jego wiarygodność!',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Hr(),

    html.Div(style={'textAlign': 'center'}, children=[
        dcc.Textarea(
            id='input_text',
            value=example,
            style={'width': '50%', 'height': 200}
        ),
        html.Br(),
        # html.Button('Lematyzuj:', id='lem_button'),
        # html.Div(id='lem_text'),

        html.Button('Weryfikuj', id='ver_button'),
        html.Hr(),
    ]),

    html.Table([
        html.Tr([html.Td(['Klasyfikator NB:']), html.Td(id='NB')]),
        html.Tr([html.Td(['Klasyfikator SVC:']), html.Td(id='SVC')]),
        html.Tr([html.Td(['Klasyfikator RF:']), html.Td(id='RF')])

    ], style={'font-size': 26})
])


@app.callback(
    [
        Output(component_id='NB', component_property='children'),
        Output(component_id='SVC', component_property='children'),
        Output(component_id='RF', component_property='children')
    ],
    Input(component_id='ver_button', component_property='n_clicks'),
    State(component_id='input_text', component_property='value')
)
def verify_text(n_clicks, text):
    if n_clicks is not None:
        df = pd.DataFrame([[text]], columns=['Text'])

        df['Text'] = df['Text'].apply(preprocessing_functions.delete_escape_chars)
        df['Text'] = df['Text'].apply(preprocessing_functions.strip_non_polish)
        df['Text'] = df['Text'].apply(preprocessing_functions.replace_whitespace)
        df['Text'] = df['Text'].apply(preprocessing_functions.lowercase_all)
        df['Text'] = df['Text'].apply(preprocessing_functions.tokenize)
        df['Text'] = df['Text'].apply(preprocessing_functions.delete_stop_words)

        df = preprocessing_functions.lemmatize(df)

        tfidf_vectorizer = load('tfidf.joblib')
        tfidf_input = tfidf_vectorizer.transform(df['Text'])

        nb_classifier = load('nb_classifier.joblib')
        svc_classifier = load('svc_classifier.joblib')
        rf_classifier = load('rf_classifier.joblib')

        nb_result = str(nb_classifier.predict(tfidf_input)[0])
        svc_result = str(svc_classifier.predict(tfidf_input)[0])
        rf_result = str(rf_classifier.predict(tfidf_input)[0])

        return nb_result, svc_result, rf_result
    else:
        return '', '', ''


if __name__ == '__main__':
    app.run_server()

