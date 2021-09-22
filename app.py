import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly
import plotly.express as px
import plotly.graph_objects as go
import json
import pandas as pd

fig3_colors = ["#6baed6", "#57a0ce", "#4292c6", "#3082be", "#2171b5", "#1361a9", "#08519c", "#0b4083", "#08306b"]

#Figure 1
consumption_electricity_df = pd.DataFrame(pd.read_csv("data/Electricity_Consumption.csv"))
years = pd.Series([2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 
        2013, 2014], name='Years')

#Figure 2
production_electricity_df = pd.DataFrame(pd.read_csv("data/Electricity_Production.csv"))
production = production_electricity_df.drop(['Code'], axis=1)

#Figure 3
access_electricity_df = pd.DataFrame(pd.read_csv("data/Access_To_Electricity.csv"))

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("World Electricity and Renewable Energy"),
    html.Div([
        dcc.Graph(id='Line', figure={}),
        dcc.Graph(id='Area', figure={})
    ],style={'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='Choropleth', figure={},
        clickData={'points': [{'text': 'Philippines'}]}),
        dcc.Slider(
        id='year-slider',
        min=2000,
        max=2014,
        value=2014,
        step=1
        ),
        html.Pre(id='year')
    ],style={'width': '60%', 'display': 'inline-block', 'padding': '0 20'}),
])


#~~~~~~~~~~~~~~~~~~~~~Back end~~~~~~~~~~~~~~~~~~~~~
#Figure 3
@app.callback(
    [dash.dependencies.Output('Choropleth', 'figure'),
    dash.dependencies.Output('year', 'children')],
    dash.dependencies.Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df3 = access_electricity_df.reindex(columns=['Country ','Code',str(selected_year)])

    choropleth_fig = go.Figure(data=go.Choropleth(locations=filtered_df3['Code'], 
        z=filtered_df3[str(selected_year)],
        text= filtered_df3['Country '],
        colorscale=fig3_colors,
        autocolorscale=False,
        reversescale=False,
        marker_line_color='#FFFFFF',
        marker_line_width=0.5,
        colorbar_title='Access %'))

    choropleth_fig.update_layout(title_text = 'Population Percentage with Access to Electricity',
        geo=dict(subunitcolor='grey', bgcolor='black', lakecolor='black', showframe=False, showcoastlines=True, 
            projection_type='equirectangular'),
        width=800, height=520,
        paper_bgcolor="black",
        plot_bgcolor='black',
        font_color="white",
        transition_duration=500)

    return choropleth_fig, str(selected_year)

#Figure 1
def create_line(fig1_df):
    temp_df = pd.concat([years, fig1_df], axis=1)
    temp_df['kWh'] = temp_df['kWh'].astype(float)

    fig1 = px.line(temp_df, x="Years", y="kWh",  title="Electricity Consumption",
        width=350, height=270)
    fig1.update_layout(
        paper_bgcolor="black",
        plot_bgcolor='black',
        font_color="white")
    fig1.update_traces(line_color='#f28e2b')

    return fig1

#Figure 2
def create_area(fig2_df):
    fig2 = px.area(fig2_df, x="Year", y=['Coal', 'Hydro', 'Solar', 'Oil', 'Wind'],
        title="Electricity Production",
        labels={'value':'tWh'}, width=350, height=270)  
    fig2.update_layout(
        paper_bgcolor="black",
        plot_bgcolor='black',
        font_color="white")

    return fig2

@app.callback(
    [dash.dependencies.Output('Line', 'figure'),
    dash.dependencies.Output('Area', 'figure')],
    dash.dependencies.Input('Choropleth', 'clickData'))
def display_click_data(clickData):
    country = clickData['points'][0]['text']
    country_data = consumption_electricity_df[consumption_electricity_df['Country'] 
    == country]
    if(len(country_data) != 0):
        test_data = pd.Series(country_data.iloc[0,2:17], name='kWh').reset_index()
    else:
        test_data = pd.Series(consumption_electricity_df.iloc[0,2:17], name='kWh').reset_index()
        for col in test_data.columns:
            test_data[col].values[:] = 0

    test_data2 = production[production['Country'] == country].reset_index()
    test_data2 = test_data2.drop(['Country', 'index'], axis=1)
    if(len(test_data2) == 0):
        for col in test_data2.columns:
            test_data2[col].values[:] = 0

    return create_line(test_data), create_area(test_data2)

if __name__ == '__main__':
    app.run_server(debug=True)