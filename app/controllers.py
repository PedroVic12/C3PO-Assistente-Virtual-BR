from dash.dependencies import Input, Output
from models import load_data, create_line_graph, create_bar_graph, create_scatter_graph

# Load data
df = load_data()

# Register callbacks
def register_callbacks(app):
    # Populate the line graph dropdown with unique country options
    @app.callback(
        Output('line-country-dropdown', 'options'),
        Input('line-country-dropdown', 'value')
    )
    def update_country_dropdown(_):
        return [{'label': country, 'value': country} for country in df['country'].unique()]

    # Update the line graph
    @app.callback(
        Output('line-graph', 'figure'),
        Input('line-country-dropdown', 'value')
    )
    def update_line_graph(selected_country):
        if selected_country is None:
            selected_country = 'United States'  # Default country
        return create_line_graph(df, selected_country)

    # Update the bar graph
    @app.callback(
        Output('bar-graph', 'figure'),
        Input('bar-year-slider', 'value')
    )
    def update_bar_graph(selected_year):
        return create_bar_graph(df, selected_year)

    # Update the scatter graph
    @app.callback(
        Output('scatter-graph', 'figure'),
        Input('scatter-year-slider', 'value')
    )
    def update_scatter_graph(selected_year):
        return create_scatter_graph(df, selected_year)

    # Update the data table with the first 10 rows
    @app.callback(
        Output('data-table', 'data'),
        Input('line-country-dropdown', 'value')
    )
    def update_table(_):
        return df.head(10).to_dict('records')
