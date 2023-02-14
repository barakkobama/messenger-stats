import plotly.express as px
import dash
from dash import dcc,Input,Output,html
import dash_daq as daq

GROUP_NAME = 'GROUP_NAME'
PARTICIPANTS ='PARTICIPANTS'
FIRST_MESSAGE = 'FIRST MESSAGE DATE'


# Create the app and layout
app = dash.Dash(__name__)

app.layout = html.Div([
                html.Div([
                    html.H2(GROUP_NAME,id='group-name'),
                    html.Div([
                        html.H2(PARTICIPANTS,id='participants'),
                        html.H2(FIRST_MESSAGE)
                    ],id='header'),
                html.Div([
                    html.Div([
                        daq.BooleanSwitch(id='daq-messages',on=False),
                        html.H2(id='messegas-title',title="Messages sent"),
                        html.Div([
                            html.H1(id='ss',title='HOLDER')
                            #dcc.Graph(...)#messages graph
                        ],id='messages-graph')
                    ],className="single-graph-holder"),
                    html.Div([
                        daq.BooleanSwitch(id='daq-words',on=False),
                        html.H2(id='words-title',title="Word count"),
                        dcc.Input(id='words-input',type='text',value='',placeholder='Enter a phrase'),
                        html.Button('Submit',id='word-button',n_clicks=0),
                        html.Div([
                            html.H1(id='ssa',title='HOLDER')
                            #dcc.Graph(...)#words graph
                        ],id='word-graph')
                    ],className="single-graph-holder")

                ],className='multi-graph-holder')
                

                ])
            ])






# Define the callback to process the input and update the output
@app.callback(
    Output('messages-graph','children'),
    Output('word-graph','children'),
    Input('daq-messages','on'),
    Input('word-button','n_clicks'),
    Input('words-input','value')
)
def update_output(n_clicks, on,value):
     return [1,2]

if __name__ == '__main__':
    app.run_server(debug=True)