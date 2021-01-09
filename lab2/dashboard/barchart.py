import plotly.express as px

def barChartAllYears(pDF):
    df1 = pDF[['total_playtime','type']].groupby(['type']).sum().reset_index()
    fig = px.bar(df1, x='type', y='total_playtime')
    return fig