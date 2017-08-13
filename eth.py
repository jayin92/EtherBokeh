import requests
import json
import time


from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import Figure, show, output_file, figure

# *********************************
address = '在這裡輸入錢包地址' #e.g. address = '0x72d8B877CD3E0EB4DBF7121d098a816068915433'
# *********************************

source = ColumnDataSource(dict(x=[], y=[], avg=[], longavg=[]))
fig = Figure(x_axis_label = 'Time',
			 y_axis_label = 'Mhash/s',
			 plot_width=1500,
			 plot_height=843)
# fig.xaxis.axis_lable = 'Time'
# fig.yaxis.axis_lable = 'Mhash/s'
fig.line(source=source, x='x', y='y',
		 line_width=2, alpha=0.85, color='red', legend='current Hashrate')
fig.line(source=source, x='x', y='avg',
		 line_width=2, alpha=0.85, color='blue', legend='average Hashrate(3hr)')
fig.line(source=source, x='x', y='longavg',
		 line_width=2, alpha=0.85, color='green', legend='average Hashrate(long)')
api_url = 'http://tweth.tw:8080/api/accounts/' + address
ct = 0
local = ''
longHashrate = 0
def update():
	global ct, local, longHashrate
	ct += 10
	times = ct / 10
	rawdata = requests.get(api_url)
	data = json.loads(rawdata.text)
	currentHashrate = data['currentHashrate'] / 1000000
	hashrate = data['hashrate'] / 1000000
	longHashrate = (currentHashrate + longHashrate)
	local = str(time.strftime("%H:%M:%S"))
	new_data = dict(x=[ct], y=[currentHashrate], avg=[hashrate], longavg=[longHashrate/times])
	source.stream(new_data, 10000)

curdoc().add_root(fig)
curdoc().add_periodic_callback(update, 10000)


