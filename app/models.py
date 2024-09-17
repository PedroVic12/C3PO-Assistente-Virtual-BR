import pandas as pd
import plotly.express as px

# Load the marketing dataset
def load_data():
    return pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

# Functions to create each graph with dynamic data filtering
def create_line_graph(df, country):
    filtered_df = df[df['country'] == country]
    return px.line(filtered_df, x='year', y='gdpPercap', title=f'GDP Over Time ({country})')

def create_bar_graph(df, year):
    filtered_df = df[df['year'] == year]
    return px.bar(filtered_df, x='continent', y='pop', title=f'Population by Continent ({year})')

def create_scatter_graph(df, year):
    filtered_df = df[df['year'] == year]
    return px.scatter(filtered_df, x='gdpPercap', y='lifeExp',
                      size='pop', color='continent', title=f'GDP vs Life Expectancy ({year})',
                      hover_name='country', log_x=True, size_max=60)
