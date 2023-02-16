#Todo:
# - Finish making graphs
# - Callbacks
# - Formating
# - Option to choose folder with messages
# - Option to specify time period
# - Maybe show most used words in list form



import plotly.express as px
import dash
from dash import dcc,Input,Output,html
import dash_daq as daq
import plotly.graph_objs as go
import msgStats

MSG_FOLDER_NAME = 'messeges'


def create_bar_chart(data_dict, title = ''):
    x_data = list(data_dict.keys())
    y_data = list(data_dict.values())

    data = [go.Bar(
                x=x_data,
                y=y_data
            )]

    layout = go.Layout(
    title = title,
    width=600, # specify the width of the plot
    height=500, # specify the height of the plot
    margin=dict(l=40, r=40, t=20, b=40) # adjust the margins
    )

    return go.Figure(data=data, layout=layout)


def create_pie_chart(data_dict, title=''):
    labels = list(data_dict.keys())
    values = list(data_dict.values())

    data = [go.Pie(
                labels=labels,
                values=values
            )]

    layout = go.Layout(
    title = title,
    width=600, # specify the width of the plot
    height=500, # specify the height of the plot
    margin=dict(l=40, r=40, t=20, b=40) # adjust the margins
    )

    return go.Figure(data=data, layout=layout)

#Getting data
files = msgStats.getFiles(MSG_FOLDER_NAME)
dataAll = [msgStats.fixData(msgStats.readFile(file)) for file in files]  #takes a long time to finish
groupName = msgStats.getGroupName(dataAll[0])
participants = msgStats.getParticipants(dataAll[0])
first_message = msgStats.getFirstMsgDate(dataAll)

#Getting data for graphs
msgCount = msgStats.countMessagesAll(dataAll,False)
wordsUsed = msgStats.countWords(dataAll,False)
reactionsRecived = msgStats.countReactionsRecivedAll(dataAll,sort=False)
reactionsGiven = msgStats.countReactionsGivenAll(dataAll,sort=False)
mostReactedTo = msgStats.mostReactedToMessage(dataAll)
mediaSent = msgStats.countMediaAll(dataAll,False)
msgLen = msgStats.countMessageLenAll(dataAll,False)
avgLen = msgStats.countAvgMessageLen(dataAll,False)
reactProp = msgStats.countReactionProp(dataAll,False)
mostUsedWords = msgStats.countWords(dataAll,False)

#Creating graphs

graphMessagesCountBar = create_bar_chart(msgCount)
graphMessagesCountPie = create_pie_chart(msgCount)  

graphWordCountBar = create_bar_chart(msgCount)  #fix that
graphWordCountPie = create_pie_chart(msgCount)

graphReactionsRecivedBar = create_bar_chart(reactionsRecived)
graphReactionsGivenBar = create_bar_chart(reactionsGiven)

graphMostUsedWords = create_bar_chart(mostUsedWords)





REACTIONS = ['ALL','👍','❤','😆','😮','👎','🤡']


MOST_REACTED_TO_MESSAGES = ['1','2','3']



app = dash.Dash(__name__)


app.layout = html.Div([
                html.Div([
                    html.H2(f'Group/person name: {groupName}',id='group-name'),
                    html.Div([
                        html.H2(f'Praticipants {participants}',id='participants'),
                        html.H2(f'Date of the first message:{first_message}')
                    ],id='header'),
                    html.Div([
                        html.Div([
                            html.H2("Messages sent",className='graph-name'),
                            html.Div([
                                html.P('Number of messages',className = 'options'),
                                daq.BooleanSwitch(id='daq-messages',on=False),
                                html.P('Procentage of all messages',className = 'options')
                            ],className='button-options'),
                            html.Div([
                                dcc.Graph(figure=graphMessagesCountBar)
                            ],id='messages-graph',className='graph')
                        ],className="single-graph-holder left-side-graph"),
                        html.Div([
                            html.H2("Word count",className='graph-name'),
                            html.Div([
                                html.P('Number of messages',className = 'options'),
                                daq.BooleanSwitch(id='daq-words',on=False),
                                html.P('Procentage of all messages',className = 'options')
                            ],className='button-options'),
                            dcc.Input(id='words-input',type='text',value='',placeholder='Enter a phrase'),
                            html.Button('Submit',id='word-button',n_clicks=0),
                            html.Div([
                                dcc.Graph(className='graph',figure=graphWordCountBar)
                            ],id='word-graph')
                        ],className="single-graph-holder right-side-graph")
                    ],className='multi-graph-holder')
                    ]),
                    html.Div([
                        html.Div([
                            html.H2("Reaction recived",className='graph-name'),
                            dcc.Dropdown(
                                className='reaction-dropdown',
                                options=REACTIONS,
                                value=REACTIONS[0]),
                            html.Div([
                                dcc.Graph(figure=graphReactionsRecivedBar)
                            ],id='reactions-recived-graph',className='graph')
                        ],className="single-graph-holder left-side-graph"),
                        html.Div([
                            html.H2("Reactions left",className='graph-name'),
                            dcc.Dropdown(
                            className='reaction-dropdown',
                            options=REACTIONS,
                            value=REACTIONS[0]),
                            html.Div([
                                dcc.Graph(className='graph',figure=graphReactionsGivenBar)
                            ],id='reactions-left-graph')
                        ],className="single-graph-holder right-side-graph")
                    ],className='multi-graph-holder'),
                    html.Div([
                            html.H2("Most used words",className='graph-name'),
                            html.Div([
                                dcc.Graph(className='graph',figure=graphMessagesCountBar)
                            ],id='most-used-words-graph')
                        ],className='single-graph-holder'),
                    html.Div([
                        html.Div([
                            html.H2("Reaction recived to messages sent proportion",className='graph-name'),
                            dcc.Dropdown(
                                className='reaction-dropdown',
                                options=REACTIONS,
                                value=REACTIONS[0]),
                            html.Div([
                                dcc.Graph(figure=graphMessagesCountBar)
                            ],id='reactions-proportion-graph',className='graph')
                        ],className="single-graph-holder left-side-graph"),
                        html.Div([
                            html.H2("Media sent",className='graph-name'),
                            html.Div([
                                dcc.Graph(className='graph',figure=graphMessagesCountBar)
                            ],id='media-graph')
                        ],className='single-graph-holder right-side-graph')
                    ],className='multi-graph-holder'),
                html.Div([
                    html.Div([
                        html.H2("Summaric length of all messages sent",className='graph-name'),
                        html.Div([
                                html.P('Summaric length',className = 'Procentage'),
                                daq.BooleanSwitch(id='daq-len',on=False),
                                html.P('Procentage of all messages',className = 'options')
                            ],className='button-options'),
                        html.Div([
                            dcc.Graph(figure=graphMessagesCountBar)
                        ],id='sum-length-graph',className='graph')
                    ],className="single-graph-holder left-side-graph"),
                    html.Div([
                        html.H2("Average message length",className='graph-name'),
                        html.Div([
                            dcc.Graph(className='graph',figure=graphMessagesCountBar)
                        ],id='avg-len-graph')
                    ],className="single-graph-holder right-side-graph")
                ],className='multi-graph-holder'),
                html.Div([
                    html.H2('Most reacted to messages'),
                    dcc.Dropdown(
                                className='reaction-dropdown',
                                options=REACTIONS,
                                value=REACTIONS[0],
                                id = 'most-reacted-to-dropdown'),
                    html.Ol([html.Li(message) for message in MOST_REACTED_TO_MESSAGES])
                ],id = 'most-reacted-to-list')
                ])


def main():
    app.run_server(debug=True)



# Define the callback to process the input and update the output
'''@app.callback(
    Output('messages-graph','children'),
    Output('word-graph','children'),
    Input('daq-messages','on'),
    Input('word-button','n_clicks'),
    Input('words-input','value')
)
def update_output(n_clicks, on,value):
     return [1,2]





'''
if __name__ == '__main__': 
    main()