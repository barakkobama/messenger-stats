import plotly.express as px
import dash
from dash import dcc
from dash import html


# Create the app and layout
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Input(id='input-box', type='text', placeholder='Enter data'),
    html.Button('Submit', id='submit-button'),
    html.Div(id='output-container'),
    dcc.Graph(id='output-graph')
])

# Define the callback to process the input and update the output
@app.callback(
    dash.dependencies.Output('output-container', 'children'),
    dash.dependencies.Output('output-graph', 'figure'),
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')]
)
def update_output(n_clicks, input_value):
    if input_value:
        # Process the input value
        processed_value = input_value.upper()
        
        # Use the processed value to create a new graph
        graph = px.line(x=[1, 2, 3], y=[4, 5, 6], title=f"Graph for {processed_value}")
        return f'Output: {processed_value}', graph
    else:
        return '', {}

if __name__ == '__main__':
    app.run_server(debug=True)