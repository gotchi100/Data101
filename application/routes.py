from application import app
from flask import render_template, url_for
import pandas as pd
import json
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go

@app.route("/")
def index():
	# blue colorscale for the maps
	fig1_colors = ["#4e79a7","#f28e2b","#e15759",
					"#76b7b2","#59a14f"]
	# fig1_colors = ["Coal":"#4e79a7","Oil":"#f28e2b","Solar":"#e15759",
	# 				"Hydro":"#76b7b2","Wind":"#59a14f"]
	fig3_colors = ["#6baed6", "#57a0ce", "#4292c6", "#3082be", "#2171b5", "#1361a9", "#08519c", "#0b4083", "#08306b"]
	country = "Costa Rica"
	year = 'Y2014'

	#graph one
	consumption_electricity_df = pd.DataFrame(pd.read_csv("data/Electricity_Consumption.csv"))
	years = pd.Series([2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 
		2013, 2014], name='Years')

	country_data = consumption_electricity_df[consumption_electricity_df['Country'] == country]
	test_data = pd.Series(country_data.iloc[0,2:17], name='kWh').reset_index()

	temp_df = pd.concat([years, test_data], axis=1)
	temp_df['kWh'] = temp_df['kWh'].astype(float)

	fig1 = px.line(temp_df, x="Years", y="kWh",  title="Electricity Consumption",
		width=350, height=270)
	fig1.update_layout(
		paper_bgcolor="black",
		plot_bgcolor='black',
		font_color="white")
	fig1.update_traces(line_color='#f28e2b')
	graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

	#Graph Two
	production_electricity_df = pd.DataFrame(pd.read_csv("data/Electricity_Production.csv"))
	production = production_electricity_df.drop(['Code'], axis=1)
	test_data2 = production[production['Country'] == country].reset_index()
	test_data2 = test_data2.drop(['Country', 'index'], axis=1)

	fig2 = px.area(test_data2, x="Year", y=['Coal', 'Hydro', 'Solar', 'Oil', 'Wind'],
		title="Electricity Production", width=350, height=270)	
	fig2.update_layout(
		paper_bgcolor="black",
		plot_bgcolor='black',
		font_color="white")
	graph2JSON = json.dumps(fig2, cls = plotly.utils.PlotlyJSONEncoder)

	# Graph three\
	access_electricity_df = pd.DataFrame(pd.read_csv("data/Access_To_Electricity.csv"))
	test_data3 = access_electricity_df.loc[:,['Country ','Code',year]]

	choropleth_fig = go.Figure(data=go.Choropleth(locations=test_data3['Code'], 
		z=test_data3[year],
		text= test_data3['Country '],
		colorscale=fig3_colors,
		autocolorscale=False,
		reversescale=False,
		marker_line_color='#313131',
		marker_line_width=0.5,
		colorbar_title='Access (%)'))
	choropleth_fig.update_layout(title_text = 'Population % with access to electricity',
		geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular'),
		width=800, height=520,
		paper_bgcolor="black",
		plot_bgcolor='black',
		font_color="white")

	# df = px.data.medals_wide()
	# fig3 = px.bar(df, x="nation", y=['gold', 'silver', 'bronze'], title="Wide=FormInput")

	graph3JSON = json.dumps(choropleth_fig, cls = plotly.utils.PlotlyJSONEncoder)

	return render_template("index.html", title = "Home", graph1JSON = graph1JSON, 
		graph2JSON = graph2JSON, graph3JSON = graph3JSON)