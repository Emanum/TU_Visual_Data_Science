import plotly.express as px

def barChartAllYears(pDF):
    df1 = pDF[['total_playtime','type']].groupby(['type']).sum().reset_index()
    fig = px.bar(df1, x='type', y='total_playtime')
    return fig

def barChartAllYearsName(pDF,top):
    df1 = pDF[['total_playtime','name']].sort_values(by='total_playtime',ascending=False).head(top).groupby(['name']).sum().reset_index()
    fig = px.bar(df1, x='name', y='total_playtime')
    return fig

def barChartPerYear(pDF):
    df1 = pDF[['total_playtime','release_year','type']].groupby(['release_year','type']).sum().reset_index()
    fig = px.bar(df1, x='release_year', y='total_playtime',color='type')
    return fig

def barChartPerYearTopN(pDF,n):
    df1 = pDF[['total_playtime','release_year','name']].sort_values(by='total_playtime',ascending=False).head(n).groupby(['release_year','name']).sum().reset_index()
    fig = px.bar(df1, x='release_year', y='total_playtime',color='name')
    return fig