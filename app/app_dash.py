import dash
import dash_bootstrap_components as dbc
from views import create_custom_layout, create_main_dashboard_layout
from controllers import register_callbacks

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Set the layout
app.layout = create_main_dashboard_layout()

# Register callbacks from the controller
register_callbacks(app)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=5080)
