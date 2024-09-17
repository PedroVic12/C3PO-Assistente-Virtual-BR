import dash
import dash_material_components as dmc
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import dash_draggable


# Função personalizada do layout de marketing
def create_custom_layout():
    return html.Div([
        dmc.NavBar(title="Marketing Dashboard"),
        
        # Layout with two columns: Left for table, right for draggable graphs
        dbc.Container(
            fluid=True,
            children=[
                dbc.Row(
                    children=[
                        # Column 1: Table with marketing data
                        dbc.Col(
                            dbc.Card(
                                children=[
                                    html.H2("Marketing Data Table"),
                                    dcc.Loading(
                                        id="loading-table",
                                        children=[dash_table.DataTable(id="data-table")],
                                        type="circle"
                                    )
                                ]
                            ), width=4
                        ),
                        # Column 2: Draggable and resizable graphs
                        dbc.Col(
                            dash_draggable.GridLayout(
                                id='draggable',
                                autoSize=True,
                                height=800,
                                width=800,
                                layout=[
                                    {"i": "line-graph", "x": 0, "y": 0, "w": 12, "h": 6, "static": False},
                                    {"i": "bar-graph", "x": 0, "y": 7, "w": 12, "h": 6, "static": False},
                                    {"i": "scatter-graph", "x": 0, "y": 14, "w": 12, "h": 6, "static": False}
                                ],
                                children=[
                                    html.Div([
                                        dcc.Graph(id='line-graph'),
                                        dcc.Dropdown(id='line-country-dropdown', options=[], placeholder="Select a Country")
                                    ]),
                                    html.Div([
                                        dcc.Graph(id='bar-graph'),
                                        dcc.Slider(id='bar-year-slider', min=1950, max=2007, step=1, value=2007,
                                                   marks={str(year): str(year) for year in range(1950, 2008, 5)})
                                    ]),
                                    html.Div([
                                        dcc.Graph(id='scatter-graph'),
                                        dcc.Slider(id='scatter-year-slider', min=1950, max=2007, step=1, value=2007,
                                                   marks={str(year): str(year) for year in range(1950, 2008, 5)})
                                    ]),
                                ]
                            ), width=8
                        )
                    ]
                )
            ]
        )
    ])


# Função principal do layout de dashboard com NavBar e seções
def create_main_dashboard_layout():
    # Text examples for sections
    text = dmc.Typography(text="Content here...", component="p", variant="body2")
    
    # Section 1: Example section using DMC
    section_1 = dmc.Section(
        id="section-1",
        orientation="columns",
        children=[text],
        cards=[{"title": "Card 1a", "size": 3}, {"title": "Card 1b"}]
    )

    # Section 2: Embed the custom marketing layout
    section_2 = dmc.Section(
        id="section-2",
        size=12,  # Full width for the custom content
        orientation="rows",
        children=[
            create_custom_layout()  # Inserindo o layout de marketing customizado
        ],
        cards=[{"title": "Marketing Dashboard", "size": 12}]
    )

    # Page that combines sections
    page = dmc.Page(orientation="columns", children=[section_1, section_2])

    # NavBar
    navbar = dmc.NavBar(title="Custom Dash with Marketing Dashboard")

    # Final layout
    layout = dmc.Dashboard(children=[navbar, page])

    return layout
