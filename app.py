#!/usr/bin/python
# -*- coding: utf-8 -*-

import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import preprocessing_functions
import pandas as pd
from joblib import load


app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

######################################################################################################################
# LAYOUT
######################################################################################################################

app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.Hr(),
        html.H2('Rozpoznawanie tzw. "fake newsów" dotyczących koronawirusa',
                style={'textAlign': 'center'}),
        html.Hr(),
        html.Br(),

        html.Div(children=[
            dbc.Textarea(id='input_text',
                         className="mb-3",
                         placeholder="Tutaj wklej treść wiadomości do zweryfikowania",
                         rows=10),
        ],
            style={'textAlign': 'center'}
        ),

        dbc.Button(
                "Weryfikuj",
                id="ver_button",
                color="primary",
                className="d-grid gap-2 col-6 mx-auto",
                n_clicks=0
        ),

        html.Br(),

        dbc.Alert(children=[
                html.H4("Werdykt:", className="alert-heading"),
                html.H2(id='verdict'),
                html.Hr(),
                html.P('Predykcje poszczególnych klasyfikatorów (True - wiadomość prawdziwa, False - fałszywa):'),
                dbc.Table(
                    [
                        html.Thead(html.Tr([html.Th("Algorytm"), html.Th("Predykcja")]))
                    ] + [html.Tbody([html.Tr([html.Td("Naiwny klasyfikator bayesowski"), html.Td(id="NB")]),
                                     html.Tr([html.Td("Liniowa maszyna wektorów nośnych"), html.Td(id="SVC")]),
                                     html.Tr([html.Td("Las losowy"), html.Td(id="RF")])])],
                    bordered=True,
                    dark=False,
                    hover=False,
                    responsive=False,
                    striped=True,
                    # style={'width': '0%'
                )
            ],
            color="secondary"
        ),
    ]
)


######################################################################################################################
# CALLBACKS
######################################################################################################################


@app.callback(
    [
        Output(component_id='verdict', component_property='children'),
        Output(component_id='NB', component_property='children'),
        Output(component_id='SVC', component_property='children'),
        Output(component_id='RF', component_property='children')
    ],
    Input(component_id='ver_button', component_property='n_clicks'),
    State(component_id='input_text', component_property='value'),
)
def get_predictions(n_clicks, text):
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

        nb_result = nb_classifier.predict(tfidf_input)[0]
        svc_result = svc_classifier.predict(tfidf_input)[0]
        rf_result = rf_classifier.predict(tfidf_input)[0]

        if not (nb_result and svc_result and rf_result):
            verdict = 'To prawdopobodnie fałszywa informacja'
        else:
            verdict = 'To prawdopobodnie prawdziwa informacja'

        return verdict, str(nb_result), str(svc_result), str(rf_result)
    else:
        return '?', '?', '?', '?'


if __name__ == '__main__':
    app.run_server(debug=False)
