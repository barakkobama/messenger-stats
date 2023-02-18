
import plotly.express as px
import dash
from dash import dcc,Input,Output,html,State
import dash_daq as daq
import plotly.graph_objs as go
import msgStats

MSG_FOLDER_NAME = 'messeges'


def create_bar_chart(data_dict, title = '',width = 600):
    x_data = list(data_dict.keys())
    y_data = list(data_dict.values())

    data = [go.Bar(
                x=x_data,
                y=y_data
            )]

    layout = go.Layout(
    title = title,
    width=width, # specify the width of the plot
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
msgCount = dict(msgStats.countMessagesAll(dataAll))
wordUsed = dict(msgStats.countGivenWordAll(dataAll,word='hello'))
wordFreqUsed = dict(msgStats.countWordFreq(dataAll,word = 'hello'))
reactionsRecived = dict(msgStats.countReactionsRecivedAll(dataAll))
reactionsGiven = dict(msgStats.countReactionsGivenAll(dataAll))
mostReactedTo = msgStats.mostReactedToMessage(dataAll)
mediaSent = dict(msgStats.countMediaAll(dataAll))
msgLen = dict(msgStats.countMessageLenAll(dataAll))
avgLen = dict(msgStats.countAvgMessageLen(dataAll))
reactProp = dict(msgStats.countReactionProp(dataAll))
mostUsedWords = dict(msgStats.countWords(dataAll,range=100))
reactionsRecivedProp = dict(msgStats.countReactionProp(dataAll))
#Creating graphs

graphMessagesCountBar = create_bar_chart(msgCount)
graphMessagesCountPie = create_pie_chart(msgCount)  

graphWordCountBar = create_bar_chart(wordUsed)
graphWordCountPie = create_bar_chart(wordFreqUsed)

graphReactionsRecivedBar = create_bar_chart(reactionsRecived)
graphReactionsGivenBar = create_bar_chart(reactionsGiven)

graphMostUsedWords = create_bar_chart(mostUsedWords,width=1300)

graphReactionsRecivedPropBar = create_bar_chart(reactionsRecivedProp)

graphMediaSent = create_bar_chart(mediaSent)

graphLenMesBar = create_bar_chart(msgLen)
graphLenMesPie = create_pie_chart(msgLen)

graphAvgLenMes = create_bar_chart(avgLen)


REACTIONS = ['all','👍','❤','😆','😮','👎','🤡']





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
                                daq.BooleanSwitch(id='switch-messages',on=False),
                                html.P('Procentage of all messages',className = 'options')
                            ],className='button-options'),
                            html.Div([
                                dcc.Graph(id='graph-messages-bar',figure=graphMessagesCountBar),
                                dcc.Graph(id='graph-messages-pie',figure=graphMessagesCountPie),
                            ],id='messages-graph',className='graph')
                        ],className="single-graph-holder left-side-graph"),
                        html.Div([
                            html.H2("Amout of times a given word was used",className='graph-name'),
                            html.Div([
                                html.P('Number of times',className = 'options'),
                                daq.BooleanSwitch(id='switch-words',on=False),
                                html.P('What procentage of messages contained given word',className = 'options')
                            ],className='button-options'),
                            dcc.Input(id='words-input',type='text',value='example',placeholder='Write here'),
                            html.Button('Submit',id='word-button',n_clicks=0),
                            html.Div([
                                dcc.Graph(id='graph-words-bar'),
                                dcc.Graph(id='graph-words-pie')
                            ],id='word-graph')
                        ],className="single-graph-holder right-side-graph")
                    ],className='multi-graph-holder')
                    ]),
                    html.Div([
                        html.Div([
                            html.H2("Reaction recived",className='graph-name'),
                            dcc.Dropdown(
                                id='reaction-recived-dropdown',
                                options=REACTIONS,
                                value=REACTIONS[0]),
                            html.Div([
                                dcc.Graph(id='graph-reactions-recived')
                            ],className='graph')
                        ],className="single-graph-holder left-side-graph"),
                        html.Div([
                            html.H2("Reactions left",className='graph-name'),
                            dcc.Dropdown(
                            id='reaction-left-dropdown',
                            options=REACTIONS,
                            value=REACTIONS[0]),
                            html.Div([
                                dcc.Graph(id='graph-reactions-left')
                            ])
                        ],className="single-graph-holder right-side-graph")
                    ],className='multi-graph-holder'),
                    html.Div([
                            html.H2("Most used words",className='graph-name'),
                            html.Div([
                                dcc.Graph(className='graph',figure=graphMostUsedWords)
                            ],id='most-used-words-graph')
                        ],className='single-graph-holder left-side-graph long-graph-holder'),
                    html.Div([
                        html.Div([
                            html.H2("Reaction recived to messages sent proportion (%)",className='graph-name'),
                            dcc.Dropdown(
                                id='reaction-prop-dropdown',
                                options=REACTIONS,
                                value=REACTIONS[0]),
                            html.Div([
                                dcc.Graph(id='graph-reaction-prop')
                            ],className='graph')
                        ],className="single-graph-holder left-side-graph"),
                        html.Div([
                            html.H2("Media sent",className='graph-name'),
                            html.Div([
                                dcc.Graph(className='graph',figure=graphMediaSent)
                            ],id='media-graph')
                        ],className='single-graph-holder right-side-graph')
                    ],className='multi-graph-holder'),
                html.Div([
                    html.Div([
                        html.H2("Summaric length of all messages sent",className='graph-name'),
                        html.Div([
                                html.P('Summaric length',className = 'Procentage'),
                                daq.BooleanSwitch(id='switch-len',on=False),
                                html.P('Procentage of all messages',className = 'options')
                            ],className='button-options'),
                        html.Div([
                            dcc.Graph(id='graph-len-bar',figure=graphLenMesBar),
                            dcc.Graph(id='graph-len-pie',figure=graphLenMesPie),
                        ],id='sum-length-graph',className='graph')
                    ],className="single-graph-holder left-side-graph"),
                    html.Div([
                        html.H2("Average message length",className='graph-name'),
                        html.Div([
                            dcc.Graph(className='graph',figure=graphAvgLenMes)
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
                    html.Ol(id='most_reacted_list')
                ],id = 'most-reacted-to-list')
                ])


def main():
    app.run_server(debug=True)



@app.callback(
    Output('graph-messages-bar', 'style'),
    Output('graph-messages-pie', 'style'),
    Input('switch-messages', 'on')
)
def toggle_graphs_messages(switch_value):
    if switch_value:
        return {'display': 'none'}, {'display': 'block'}
    else:
        return {'display': 'block'}, {'display': 'none'}



@app.callback(
    Output('graph-words-bar', 'style'),
    Output('graph-words-pie', 'style'),
    Output('graph-words-bar', 'figure'),
    Output('graph-words-pie', 'figure'),
    Input('switch-words', 'on'),
    Input('word-button', 'n_clicks'),
    State('words-input', 'value')
)
def toggle_graphs_words(switch_value,n_clicks,value):
    graphWordCountPie =create_bar_chart(dict(msgStats.countWordFreq(dataAll,word=value)))
    graphWordCountBar =create_bar_chart(dict(msgStats.countGivenWordAll(dataAll,word=value)))

    if switch_value:
        return {'display': 'none'}, {'display': 'block'},graphWordCountBar,graphWordCountPie
    else:
        return {'display': 'block'}, {'display': 'none'},graphWordCountBar,graphWordCountPie
    
@app.callback(
    Output('graph-reactions-recived', 'figure'),
    Input('reaction-recived-dropdown', 'value')
)
def toggle_graphs_reactions_recived(value):
    graphReactionsRecivedBar =create_bar_chart(dict(msgStats.countReactionsRecivedAll(dataAll,whatReaction=value)))
    return graphReactionsRecivedBar

@app.callback(
    Output('graph-reactions-left', 'figure'),
    Input('reaction-left-dropdown', 'value')
)
def toggle_graphs_reactions_left(value):
    graphReactionsLeftBar =create_bar_chart(dict(msgStats.countReactionsGivenAll(dataAll,whatReaction=value)))
    return graphReactionsLeftBar


@app.callback(
    Output('graph-reaction-prop', 'figure'),
    Input('reaction-prop-dropdown', 'value')
)
def toggle_graphs_reactions_prop(value):
    graphReactionsPropBar =create_bar_chart(dict(msgStats.countReactionProp(dataAll,whatReaction=value)))
    return graphReactionsPropBar



@app.callback(
    Output('graph-len-bar', 'style'),
    Output('graph-len-pie', 'style'),
    Input('switch-len', 'on')
)
def toggle_graphs_messages(switch_value):
    if switch_value:
        return {'display': 'none'}, {'display': 'block'}
    else:
        return {'display': 'block'}, {'display': 'none'}


[html.Li(str(message)) for message in mostReactedTo],

@app.callback(
    Output('most_reacted_list', 'children'),
    Input('most-reacted-to-dropdown', 'value')
)
def toggle_graphs_reactions_left(value):
    mostReactedTo = [html.Li(str(message)) for message in msgStats.mostReactedToMessage(dataAll,value)]
    return mostReactedTo
    





if __name__ == '__main__': 
    main()