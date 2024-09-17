import dash
import dash_material_components as dmc
from dash import html, dcc, Input, Output, dash_table
import plotly.express as px
import pandas as pd

# Load dataset
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

# Instantiate Dash app
app = dash.Dash(__name__)

# Create graphs functions
def create_line_graph(country):
    filtered_df = df[df['country'] == country]
    fig = px.line(filtered_df, x='year', y='gdpPercap', title=f'GDP Over Time ({country})')
    return fig

def create_bar_graph(year):
    filtered_df = df[df['year'] == year]
    fig = px.bar(filtered_df, x='continent', y='pop', title=f'Population by Continent ({year})')
    return fig

def create_scatter_graph(year):
    filtered_df = df[df['year'] == year]
    fig = px.scatter(filtered_df, x='gdpPercap', y='lifeExp', size='pop', color='continent',
                     title=f'GDP vs Life Expectancy ({year})', hover_name='country', log_x=True, size_max=60)
    return fig

# Layout for the app
app.layout = dmc.MantineProvider(
    withGlobalStyles=True,
    withNormalizeCSS=True,
    children=[
        dmc.Paper(
            shadow="md",
            radius="lg",
            p="xl",
            children=[
                dmc.Text("Marketing Dashboard", weight=700, size="xl", align="center", color="blue"),
                dmc.Grid(
                    children=[
                        # Left column: Data Table
                        dmc.Col(
                            span=4,
                            children=[
                                dmc.Card(
                                    shadow="sm",
                                    p="md",
                                    children=[
                                        dmc.Text("Marketing Data Table", size="lg"),
                                        dash_table.DataTable(
                                            id="data-table",
                                            columns=[{"name": i, "id": i} for i in df.columns],
                                            data=df.to_dict('records'),
                                            page_size=10
                                        )
                                    ]
                                )
                            ]
                        ),
                        # Right column: Draggable graphs
                        dmc.Col(
                            span=8,
                            children=[
                                dmc.Card(
                                    shadow="sm",
                                    p="md",
                                    children=[
                                        dmc.Text("GDP Over Time"),
                                        dcc.Dropdown(
                                            id='line-country-dropdown',
                                            options=[{'label': country, 'value': country} for country in df['country'].unique()],
                                            value='United States',
                                            clearable=False
                                        ),
                                        dcc.Graph(id='line-graph')
                                    ]
                                ),
                                dmc.Card(
                                    shadow="sm",
                                    p="md",
                                    mt="md",
                                    children=[
                                        dmc.Text("Population by Continent (Adjust Year)"),
                                        dcc.Slider(
                                            id='bar-year-slider', min=1950, max=2007, step=1, value=2007,
                                            marks={str(year): str(year) for year in range(1950, 2008, 5)}
                                        ),
                                        dcc.Graph(id='bar-graph')
                                    ]
                                ),
                                dmc.Card(
                                    shadow="sm",
                                    p="md",
                                    mt="md",
                                    children=[
                                        dmc.Text("GDP vs Life Expectancy (Adjust Year)"),
                                        dcc.Slider(
                                            id='scatter-year-slider', min=1950, max=2007, step=1, value=2007,
                                            marks={str(year): str(year) for year in range(1950, 2008, 5)}
                                        ),
                                        dcc.Graph(id='scatter-graph')
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

# Callbacks to update graphs
@app.callback(
    Output('line-graph', 'figure'),
    Input('line-country-dropdown', 'value')
)
def update_line_graph(selected_country):
    return create_line_graph(selected_country)

@app.callback(
    Output('bar-graph', 'figure'),
    Input('bar-year-slider', 'value')
)
def update_bar_graph(selected_year):
    return create_bar_graph(selected_year)

@app.callback(
    Output('scatter-graph', 'figure'),
    Input('scatter-year-slider', 'value')
)
def update_scatter_graph(selected_year):
    return create_scatter_graph(selected_year)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
