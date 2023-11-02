import logging
import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go

from pymongo import MongoClient


def get_mongodb_data():
    try:
        userData = []
        #=> connecting to the cassandra cluster
        client = MongoClient(host="localhost",port=27023)

        db = client["user_db"]

        col = db['user_profiles']

        for c in col.find({}):
            userData.append(dict({'age':c['age'],'nat':c['nat'],'gender':c['gender'],'domain':c['email_domain']}))

        return userData
    except Exception as e:
        logging.error(f"Could not create mongodb connection due to {e}")
        return None

#df = pd.DataFrame(get_mongodb_data())

colors = ["mediumturquoise", "gold", "darkorange", "lightgreen"]

#print(df_count_of_domain)

external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]

app = Dash(__name__,external_stylesheets=external_stylesheets)

app.layout =  html.Div(children=[
    html.Div(
            children=[
                html.H1(
                    children="User Analytics", className="header-title",
                ),
            ],
            className="header",),

            #=> count of user by nationality
            html.Div(id='live-update-nat-graph'),
        
             #=> avg of age by nationality
            html.Div(id='live-update-age-avg-graph'),

            #=> count of domain name
            html.Div(id='live-update-domain-graphs'),

            #Intervale
            dcc.Interval(
                id='interval-component',
                interval=1*1000, # in milliseconds
                n_intervals=0
            ),
            ])


@callback(Output('live-update-nat-graph', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    
    ##style = {'padding': '5px', 'fontSize': '16px'}
    df = pd.DataFrame(get_mongodb_data())

   # #count of user by nationality
    df_user_by_nat = df.groupby('nat')['nat'].count().reset_index(name='count')

    return [
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": df_user_by_nat["nat"],
                        "y": df_user_by_nat["count"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Nombre d'utilisateurs par nationalité"},
            },
            ),
    ]

@callback(Output('live-update-age-avg-graph', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    
    ##style = {'padding': '5px', 'fontSize': '16px'}
    df = pd.DataFrame(get_mongodb_data())
    #print(df)

    #avg of age by nationality
    df_user_age_avg = df.groupby('nat')['age'].mean().round(0).reset_index(name='avg')

    return [
        #dash
        dcc.Graph(
        figure={
            "data": [
                {
                    "x": df_user_age_avg["nat"],
                    "y": df_user_age_avg["avg"],
                    "type": "bar",
                },
            ],
            "layout": {"title": "Âge moyen des utilisateurs"},
        },
        ),
    ] 

@callback(Output('live-update-domain-graphs', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    
    ##style = {'padding': '5px', 'fontSize': '16px'}
    df = pd.DataFrame(get_mongodb_data())

    #count of domain name
    df_count_of_domain = df.groupby('domain')['domain'].count().reset_index(name='count')

    return [
        html.Div(children=[
            #dash
            dcc.Graph(
            figure={
                "data": [
                    {
                        "x": df_count_of_domain["domain"],
                        "y": df_count_of_domain["count"],
                        "type": "bar",
                        "width" : 0.1
                    },
                ],
                "layout": {"title": "Domaines de courriel les plus courants"},
            },
            ),
            ],style={'width': '48%', 'align': 'right', 'display': 'inline-block'}),
            
            html.Div(children=[
                dcc.Graph(
                    figure={
                        "data":[
                            go.Pie(
                                labels=df_count_of_domain['domain'],
                                values=df_count_of_domain['count'],
                                textfont_size=20,
                                marker=dict(colors=colors)
                            )
                        ],
                        "layout": {"title": " Pourcentage des Domaines les plus courants"},
                    }
                )
            ],
            style={'width': '48%', 'align': 'right', 'display': 'inline-block'}
            ),
    ] 

if __name__ == "__main__":
    app.run_server(debug=True)