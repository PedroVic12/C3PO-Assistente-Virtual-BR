import dash
import dash_material_components as dmc 
from dash import html, dcc, dash_table 
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_draggable
import dash_bootstrap_components as dbc

# Load dataset
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

# Instantiate a Dash app
app = dash.Dash(__name__)

# Create graphs
def create_line_graph():
    fig = px.line(df[df['country'] == 'United States'], x='year', y='gdpPercap', title='GDP Over Time (US)')
    return fig

def create_bar_graph():
    fig = px.bar(df[df['year'] == 2007], x='continent', y='pop', title='Population by Continent (2007)')
    return fig

def create_scatter_graph():
    fig = px.scatter(df[df['year'] == 2007], x='gdpPercap', y='lifeExp',
                     size='pop', color='continent', title='GDP vs Life Expectancy (2007)',
                     hover_name='country', log_x=True, size_max=60)
    return fig

# Create a table
def create_table(dataframe):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), 10))  # Limit to 10 rows
        ])
    ])

# Compose layout
app.layout = html.Div([
    dmc.NavBar(title="Dashboard with Draggable Components"),
    
    # Layout with two columns: Left for table, right for draggable graphs
    dbc.Container(
        fluid=True,
        children=[
            dbc.Row(
                children=[
                    dbc.Col(
                        
                         
                        
                        
                        # Column 1: Table
                        dbc.Card(
                            children=[
                                html.H2("Data Table (First 10 Rows)"),
                                create_table(df),
                            ]
                        ),
                    ),
                    dbc.Col(
                        # Column 2: Draggable graphs
                        dash_draggable.GridLayout(
                            id='draggable',
                            layout=[
                                {"i": "line-graph", "x": 0, "y": 0, "w": 12, "h": 6, "static": False},
                                {"i": "bar-graph", "x": 0, "y": 7, "w": 12, "h": 6, "static": False},
                                {"i": "scatter-graph", "x": 0, "y": 14, "w": 12, "h": 6, "static": False}
                            ],
                            children=[
                                dcc.Graph(id='line-graph', figure=create_line_graph()),
                                dcc.Graph(id='bar-graph', figure=create_bar_graph()),
                                dcc.Graph(id='scatter-graph', figure=create_scatter_graph())
                            ]
                        ),
                    )
                ]
            )
        ]
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=5080)
