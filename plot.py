import plotly.express as px

def create_plot(df):
    # Create a Plotly line chart
    fig = px.line(df, x=df.index, y='Portfolio_DCA', 
                  title='DCA Portfolio Value Over Time',
                  labels={'x': 'Date', 'Portfolio_DCA': 'Portfolio Value ($)'},
                  template='plotly_dark')  # Using a dark theme for a more modern look

    # Adding customizations
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Portfolio Value ($)',
        xaxis=dict(
            showline=True,
            showticklabels=True,
            ticks='outside',
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showline=True,
            showticklabels=True,
            ticks='outside',
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        legend=dict(
            x=0.01,
            y=0.99,
            traceorder='normal',
            font=dict(
                family='sans-serif',
                size=12,
                color='white'
            ),
            bgcolor='Black',
            bordercolor='Black',
            borderwidth=2
        )
    )
    return fig
