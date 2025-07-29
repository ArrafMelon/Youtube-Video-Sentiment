import utils.commentScraper as commentScraper
import utils.sentimentScore as sentimentScore
import utils.graph as graph
from dash import Dash, html, dcc, Input, Output
import plotly.graph_objs as go

app = Dash(__name__)

app.layout = html.Div(
    style={
        'fontFamily': 'Arial, sans-serif',
        'minHeight': '100vh',         
        'width': '100vw',           
        'backgroundColor': '#282828',
        'color': '#ffffff',
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'padding': '20px',
        'boxSizing': 'border-box',
    },
    children=[
        html.Div(
            style={
                'maxWidth': '900px',
                'width': '100%',
                'flexGrow': 1,
                'display': 'flex',
                'flexDirection': 'column',
                'justifyContent': 'flex-start',
            },
            children=[
                html.H1(
                    "YouTube Comment Sentiment Dashboard",
                    style={
                        'textAlign': 'center',
                        'color': '#D42B12',
                        'marginBottom': '40px'
                    }
                ),

                html.Div([
                    dcc.Input(
                        id='url-input', type='text', placeholder='Enter YouTube URL or Video ID',
                        style={
                            'width': '70%',
                            'padding': '10px',
                            'fontSize': '16px',
                            'borderRadius': '5px',
                            'border': 'none',
                            'outline': 'none'
                        }
                    ),
                    html.Button('Analyze', id='analyze-btn', n_clicks=0, style={
                        'padding': '10px 20px',
                        'marginLeft': '10px',
                        'fontSize': '16px',
                        'backgroundColor': '#D42B12',
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': '5px',
                        'cursor': 'pointer',
                        'transition': 'background-color 0.3s ease',
                    }),
                ], style={'textAlign': 'center', 'marginBottom': '30px'}),

                dcc.Loading(
                    dcc.Graph(
                        id='sentiment-graph',
                        style={
                            'flexGrow': 1,     
                            'minHeight': '400px',  
                        }
                    ),
                    type='circle',
                    style={'textAlign': 'center', 'flexGrow': 1}
                ),

                html.Div(
                    id='footer',
                    style={
                        'textAlign': 'center',
                        'marginTop': '40px',
                        'color': '#aaaaaa',
                        'fontSize': '14px'
                    },
                    children=[
                        "Built with ", html.A("Dash", href="https://dash.plotly.com/", target="_blank", style={'color': '#D42B12', 'textDecoration': 'none'}), " and Plotly"
                    ]
                )
            ]
        )
    ]
)

@app.callback(
    Output('sentiment-graph', 'figure'),
    Input('analyze-btn', 'n_clicks'),
    Input('url-input', 'value')
)
def update_graph(n_clicks, url):
    if not n_clicks or not url:
        return go.Figure(
            layout=go.Layout(
                title="Enter a YouTube video URL or ID and click Analyze",
                xaxis={'visible': False},
                yaxis={'visible': False},
                annotations=[{
                    'text': "Your sentiment dashboard will appear here.",
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 20, 'color': '#D42B12'}
                }],
                plot_bgcolor='#282828',
                paper_bgcolor='#282828',
                font={'color': '#ffffff'},
                height=600,  #
            )
        )
    fig = graph.make_graph(url)
    fig.update_layout(plot_bgcolor='#282828', paper_bgcolor='#282828', font_color='#ffffff', height=600)
    return fig

if __name__ == '__main__':
    app.run(debug=True)
