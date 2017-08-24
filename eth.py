import requests
import json
import time


from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import Figure, show, output_file, figure
from bokeh.models.widgets import Slider

from datetime import datetime

def multi(List):
	results = 0
	for item in List:
		results += item
	return results

source = ColumnDataSource(dict(x=[], y=[], avg=[], longavg=[]))

fig = Figure(x_axis_label = 'Time',
			 y_axis_label = 'Mhash/s',
			 x_axis_type = 'datetime',
			 plot_width=1500,
			 plot_height=800)

fig.line(source=source, x='x', y='y',
		 line_width=2, alpha=0.85, color='red', legend='current Hashrate')

fig.line(source=source, x='x', y='avg',
		 line_width=2, alpha=0.85, color='blue', legend='average Hashrate(3HR)')

fig.line(source=source, x='x', y='longavg',
		 line_width=2, alpha=0.85, color='green', legend='average Hashrate(24HR)')


updateTime = 60

##########################IMPORTANT##########################
ethereum_address = 'YOUR ADDRESS'
########YOU HAVE TO ENTER YOUR ETHEREUM ADDRESS ABOVE########


api_url = 'https://www.tweth.tw/api/accounts/' + ethereum_address
ct = 0
local = ''
longHashrate = 0
fmt = "%Y/%m/%d %H:%M:%S"
listHash = []

def update():
	global ct, local, longHashrate
	if not ct == 1440:
		ct += 1
	else:
		ct = 1440
	rawdata = requests.get(api_url)
	data = json.loads(rawdata.text)
	currentHashrate = data['currentHashrate'] / 1000000
	if len(listHash) == 1440:
		listHash.pop(0)
	listHash.append(currentHashrate)
	hashrate = data['hashrate'] / 1000000
	longHashrate = (currentHashrate + longHashrate)
	local = datetime.now()
	print(local)
	new_data = dict(x=[local], y=[currentHashrate], avg=[hashrate], longavg=[multi(listHash)/ct])
	source.stream(new_data, updateTime * 1000)

curdoc().add_root(fig)
curdoc().add_periodic_callback(update, updateTime * 1000)


