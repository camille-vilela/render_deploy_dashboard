#  Importando as bibliotecas

import pandas as pd
import numpy as np
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update

# Escolhendo o Tema

app = dash.Dash(external_stylesheets=[dbc.themes.LUX])


# Carregando os dados

df = pd.read_csv("OneDrive/Documentos/Shopping_Behavior/shopping_behavior_updated.csv")



# Top 5 Itens Mais Vendidos

top_items = df['Item Purchased'].value_counts().sort_values(ascending=False).head(5)

# Top 10 Cidades Com Mais Vendas

list_locations = list(df['Location'].value_counts().sort_values(ascending=False).head(10).index)

# Contagem de Quantas Vezes Cada Método de Pagamento foi Usado

count_payment = df['Payment Method'].value_counts().sort_values(ascending=False)

# Layout

app.layout = html.Div(children=[

    html.H1(
        children='Shopping Behavior Dashboard',
        style={
            'textAlign': 'center',
            'fontFamily': 'Roboto',
            'paddingTop': 20
        }
    ),

    html.Div(children='Choose the location to analyse.'),

    dcc.Dropdown(
        options=list_locations,
        value='Montana',
        id='list-cities'
    ),
     dbc.Row(
        [
            dbc.Col(dcc.Graph(id='category-graph'), md=7),
            dbc.Col(dcc.Graph(id='top_5_items_graph'), md=5),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id='payment_graph'), md=8)
        ]
    )
                
    ]
)

# Callback

@app.callback(
    Output('category-graph', 'figure'),
    Output('top_5_items_graph', 'figure'),
    Output('payment_graph', 'figure'),
    Input('list-cities', 'value')
)

def update_output(value):

    # Filtra por cidade
    filtered_table = df[df['Location'] == value]

    # Gráfico 1: Qtdd Comprada x Categoria
    fig1 = px.bar(
        filtered_table,
        x="Category",
        y="Purchase Amount (USD)",
        color="Gender",
        barmode="group",
        title="Purchase Amount by Category and Gender",
        color_discrete_sequence=px.colors.qualitative.Dark2
    )

    # Gráfico 2: Top 5 produtos Mais Vendidos
    top_items = (
        filtered_table['Item Purchased']
        .value_counts()
        .head(5)
    )

    fig2 = px.pie(
        values= top_items.values,
        names=top_items.index,
        title='Percentage of Sales - 5 Best-Selling Items',
        hole=0.7,
        color_discrete_sequence=px.colors.qualitative.Dark2
    )

    # Gráfico 3: Forma de pagamento
    count_payment = (
        filtered_table['Payment Method']
        .value_counts()
    )

    fig3 = px.bar(
        x=count_payment.values,
        y=count_payment.index,
        orientation="h",
        title="Payment Type Count",
        color_discrete_sequence=px.colors.qualitative.Dark2
    )

    return fig1, fig2, fig3

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8050', debug=False)
