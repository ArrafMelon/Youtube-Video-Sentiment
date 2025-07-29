from . import sentimentScore
import matplotlib.pyplot as plt
import  seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.gridspec as gridspec
from textwrap import wrap
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import urllib.parse

def video_id(value):
    """
    Extract the YouTube video ID from various YouTube URL formats.

    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&hl=en_US
    """
    query = urllib.parse.urlparse(value)
    hostname = query.hostname
    if not hostname:
        return None

    if hostname == 'youtu.be':
        return query.path[1:]
    if hostname in ('www.youtube.com', 'youtube.com', 'm.youtube.com'):
        if query.path == '/watch':
            p = urllib.parse.parse_qs(query.query)
            return p.get('v', [None])[0]
        if query.path.startswith('/embed/'):
            return query.path.split('/')[2]
        if query.path.startswith('/v/'):
            return query.path.split('/')[2]
    # fail
    return None

def make_graph(id):
    """
    Sentiment Dashboard
    """
    vid = video_id(id)
    df = sentimentScore.get_score(vid)

    df = df.rename(columns={'Number of Likes': 'Likes'})
    # Pie chart data
    sentiment_counts = df['Predicted_class'].value_counts().sort_index()
    sentiment_labels = ['Negative', 'Neutral', 'Positive']
    colors = ['#ff6f69', '#ffeead', '#96ceb4']

    top_pos = df[df['Predicted_class'] == 2].nlargest(3, 'Likes')[['Author', 'Comment', 'Likes']]
    top_neg = df[df['Predicted_class'] == 0].nlargest(3, 'Likes')[['Author', 'Comment', 'Likes']]
    top_neu = df[df['Predicted_class'] == 1].nlargest(3, 'Likes')[['Author', 'Comment', 'Likes']]

    # Wrap comments
    def wrap_comments(comments, width=50):
        return ['<br>'.join(wrap(str(c), width)) for c in comments]

    top_pos['Comment'] = wrap_comments(top_pos['Comment'])
    top_neg['Comment'] = wrap_comments(top_neg['Comment'])

    fig = make_subplots(
        rows=2, cols=3,
        specs=[[{"type": "table"}, {"type": "table"}, {"type": "table"}],  
            [{"type": "bar"}, {"type": "pie"}, {"type": "bar"}]],
        column_widths=[0.33, 0.34, 0.33],  
        row_heights=[0.3, 0.7],
        vertical_spacing=0.12,
        horizontal_spacing=0.05,
        subplot_titles=(
            "Top 3 Positive Comments",
            "Top 3 Neutral Comments",
            "Top 3 Negative Comments",
            "Total Likes per Sentiment",
            "",
            "Average Likes per Sentiment"
        )
    )

    # Positive Comments Table
    fig.add_trace(go.Table(
        columnwidth=[0.2, 0.65, 0.15], 
        header=dict(
            values=["Author", "Comment", "Likes"],
            fill_color='#96ceb4',
            font=dict(color='white', size=12),
            align=['left', 'left', 'center'],
        ),
        cells=dict(
            values=[top_pos[col] for col in top_pos.columns],
            fill_color=[['#d4f0e7', 'white', '#d4f0e7']],
            align=['left', 'left', 'center'],
            font=dict(color='black', size=11),
        )
    ), row=1, col=1)

    # Neutral Comments Table
    fig.add_trace(go.Table(
        columnwidth=[0.2, 0.65, 0.15], 
        header=dict(
            values=["Author", "Comment", "Likes"],
            fill_color='#ffeead',
            font=dict(color='white', size=12),
            align=['left', 'left', 'center'],
        ),
        cells=dict(
            values=[top_neu[col] for col in top_neu.columns],
            fill_color=[['#fff9d1', 'white', '#fff9d1']],
            align=['left', 'left', 'center'],
            font=dict(color='black', size=11),
        )
    ), row=1, col=2)

    fig.add_trace(go.Pie(
        labels=sentiment_labels,
        values=sentiment_counts,
        marker_colors=colors,
        hole=0.4,
        hoverinfo='label+percent+value',
        textinfo='percent',
        textfont_size=14,
        sort=False,
        direction='clockwise',
        showlegend=False,
        marker=dict(line=dict(color='black', width=0.5)),
        domain=dict(x=[0.34, 0.66], y=[0.35, 0.85])
    ), row=2, col=2)

    # Negative Comments Table
    fig.add_trace(go.Table(
        columnwidth=[0.2, 0.65, 0.15],
        header=dict(
            values=["Author", "Comment", "Likes"],
            fill_color='#ff6f69',
            font=dict(color='white', size=12),
            align=['left', 'left', 'center'],
        ),
        cells=dict(
            values=[top_neg[col] for col in top_neg.columns],
            fill_color=[['#f9d6d5', 'white', '#f9d6d5']],
            align=['left', 'left', 'center'],
            font=dict(color='black', size=11),
        )
    ), row=1, col=3)

    # Sum of likes per class
    likes_sum = df.groupby('Predicted_class')['Likes'].sum().reindex([0,1,2])
    likes_sum = likes_sum.fillna(0)
    # Total Likes Bar Chart
    fig.add_trace(go.Bar(
        x=sentiment_labels,
        y=likes_sum,
        marker_color=colors,
        text=[f"{int(x):,}" for x in likes_sum],
        textposition='outside',
        name='Total Likes'
    ), row=2, col=1)

    # Average likes per class
    likes_avg = df.groupby('Predicted_class')['Likes'].mean().reindex([0,1,2]).fillna(0)
    # Average Likes Bar Chart
    fig.add_trace(go.Bar(
        x=sentiment_labels,
        y=likes_avg,
        marker_color=colors,
        text=[f"{x:.1f}" for x in likes_avg],
        textposition='outside',
        name='Average Likes'
    ), row=2, col=3)

    # Final Layout
    fig.update_layout(
        height=850,
        width=1300,
        title_text="YouTube Video Sentiment",
        title_x=0.5,
        title_font_size=24,
        showlegend=False,
        margin=dict(t=100, b=50),
        plot_bgcolor='white',
        paper_bgcolor='rgba(250,250,250,1)'
    )

    return fig