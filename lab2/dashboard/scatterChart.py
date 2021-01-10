import plotly.express as px

def scatterChart(df,xCol,yCol,col,siz):
    fig = px.scatter(df,x=xCol,y=yCol,color=col,size=siz,hover_name="name", hover_data=[xCol, yCol,col,siz])
    return fig