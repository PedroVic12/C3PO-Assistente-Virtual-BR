import dash_ag_grid as dag
from dash import Dash, html, dcc, Input, Output, State, callback
import pandas as pd
import plotly.express as px
from dataclasses import dataclass

app = Dash(__name__)

# Carregando e preparando os dados
df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/ag-grid/olympic-winners.csv"
)
df['marketability_score'] = (df['gold'] * 3 + df['silver'] * 2 + df['bronze']) / df['total']
df['career_span'] = df.groupby('athlete')['year'].transform('max') - df.groupby('athlete')['year'].transform('min')

@dataclass
class MainTableComponent:
    columnDefs = [
        {"field": "athlete", "lockVisible": True, "checkboxSelection": True},
        {"field": "country"},
        {"field": "sport"},
        {"field": "year"},
        {"field": "gold"},
        {"field": "silver"},
        {"field": "bronze"},
        {"field": "total"},
        {"field": "marketability_score", "valueFormatter": {"function": "d3.format('.2f')(params.value)"}},
        {"field": "career_span"}
    ]

    @staticmethod
    def render():
        return dag.AgGrid(
            id="main-table",
            rowData=df.to_dict("records"),
            columnDefs=MainTableComponent.columnDefs,
            columnSize="sizeToFit",
            suppressDragLeaveHidesColumns=False,
            dashGridOptions={"animateRows": False, "rowSelection": "multiple"}
        )

@dataclass
class ScatterPlotComponent:
    @staticmethod
    def render():
        return html.Div([
            dcc.Dropdown(
                id='y-axis-selector',
                options=[
                    {'label': 'Idade', 'value': 'age'},
                    {'label': 'Total de Medalhas', 'value': 'total'},
                    {'label': 'Tempo de Carreira', 'value': 'career_span'}
                ],
                value='age',
                style={'width': '50%'}
            ),
            dcc.Graph(id="scatter-plot")
        ])

@dataclass
class TopAthletesComponent:
    columnDefs = [
        {"field": "athlete"},
        {"field": "sport"},
        {"field": "country"},
        {"field": "marketability_score", "valueFormatter": {"function": "d3.format('.2f')(params.value)"}},
        {"field": "total"},
        {"field": "age"}
    ]

    @staticmethod
    def render():
        return html.Div([
            html.H3("Top 10 Atletas por Esporte"),
            dcc.Dropdown(
                id='sport-dropdown',
                options=[{'label': 'Todos', 'value': 'All'}] + 
                        [{'label': sport, 'value': sport} for sport in df['sport'].unique()],
                value='All',
                style={'width': '50%'}
            ),
            dag.AgGrid(
                id="top-athletes-table",
                columnDefs=TopAthletesComponent.columnDefs,
                rowData=[],
                columnSize="sizeToFit",
                dashGridOptions={"animateRows": True}
            ),
            dcc.Graph(id="line-chart")
        ])

@dataclass
class AppLayout:
    @staticmethod
    def layout():
        return html.Div([
            html.H1("Dashboard de Marketing de Atletas Olímpicos"),
            html.Button("Mostrar Todas as Colunas", id="btn-column-show-all"),
            html.Div([
                html.Div([MainTableComponent.render()], className="six columns"),
                html.Div([ScatterPlotComponent.render()], className="six columns")
            ], className="row"),
            TopAthletesComponent.render()
        ])

@dataclass
class AppCallbacks:
    @staticmethod
    def register_callbacks():
        @callback(
            Output("main-table", "columnDefs"),
            Input("btn-column-show-all", "n_clicks"),
            State("main-table", "columnDefs"),
            prevent_initial_call=True,
        )
        def show_all_columns(_, column_defs):
            for col in column_defs:
                col['hide'] = False
            return column_defs

        @callback(
            Output("scatter-plot", "figure"),
            Input("main-table", "selectedRows"),
            Input("y-axis-selector", "value")
        )
        def update_scatter_plot(selected_rows, y_axis):
            if not selected_rows:
                plot_df = df.head(50)
            else:
                plot_df = pd.DataFrame(selected_rows)
            
            return px.scatter(plot_df, x='marketability_score', y=y_axis, 
                              color='sport', size='total', hover_name='athlete',
                              title=f'Marketability Score vs {y_axis}')

        @callback(
            Output("top-athletes-table", "rowData"),
            Output("line-chart", "figure"),
            Input("sport-dropdown", "value"),
            Input("top-athletes-table", "columnState")
        )
        def update_top_athletes_and_line_chart(selected_sport, column_state):
            if selected_sport == "All":
                filtered_df = df
            else:
                filtered_df = df[df['sport'] == selected_sport]
            
            top_athletes = filtered_df.sort_values('marketability_score', ascending=False).head(10)
            
            # Reordenar as colunas de acordo com o estado da tabela
            if column_state:
                column_order = [col['colId'] for col in column_state]
                top_athletes = top_athletes[column_order]
            
            x_col, y_col = top_athletes.columns[:2]
            
            if pd.api.types.is_numeric_dtype(top_athletes[x_col]) and pd.api.types.is_numeric_dtype(top_athletes[y_col]):
                fig = px.line(top_athletes, x=x_col, y=y_col, title=f'{y_col} vs {x_col}')
            else:
                fig = {
                    'data': [],
                    'layout': {
                        'title': 'As duas primeiras colunas devem ser numéricas para gerar o gráfico de linha',
                        'xaxis': {'visible': False},
                        'yaxis': {'visible': False},
                    }
                }
            
            return top_athletes.to_dict('records'), fig

# Configuração do layout do app
app.layout = AppLayout.layout()

# Registro dos callbacks
AppCallbacks.register_callbacks()

if __name__ == "__main__":
    app.run(debug=True)