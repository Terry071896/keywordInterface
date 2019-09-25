import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
from datetime import datetime
#import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import requests
from fakeData import FactoryData
from fakeBinary import FakeKeywordValues
from keywords import Keywords

process_names = [
    'cycle_time',
    'time_to_complete',
    'safety_materials',
    'safety_manufacturing',
    'safety_packing',
    'precursor_level',
    'reagent_level',
    'catalyst_level',
    'packaging_level',
    'production_levels',
]


def get_keyword(server, keyword):
    if mode == 'local':
        proc = subprocess.Popen("show -terse -s %s %s " % (server, keyword), stdout=subprocess.PIPE, shell=True)
        result = proc.communicate()
    elif mode == 'ktlpython':
        proc = ktl.cache(server, keyword)
        result = proc.read()
    elif mode == 'web':
        url = 'http://localhost:5002/show?server=%s&keyword=%s' % (server, keyword)
        try:
            response = requests.get(url)
            ##print(response.json())
        except requests.exceptions.RequestException as e:
            #print("Error in getting data from the server")
            return
        result = response.json()
    elif mode == 'simulate':
    	return 164
    return result

mode = 'web'

binary_keywords = []
for i in ['A','B','C']:
	for j in range(1,9):
		binary_keywords.append('PWSTAT'+i+str(j))
for i in ['A','B','C']:
	for j in range(1,9):
		binary_keywords.append('PWLOC'+i+str(j))
#for i in range(0,3):
#	binary_keywords.append('LMP'+str(i)+'SHST')
#	binary_keywords.append('LMP'+str(i)+'STAT')
#binary_keywords.append('LMP3STAT')
#for i in ['BRANGE', 'RRANGE']:
#	for j in range(1,3):
#		binary_keywords.append(i+str(j))
#binary_keywords.append('BROCHM')
#binary_keywords.append('BVHVON')

server = []
for x in binary_keywords:
	server.append('kcwi')

fdata = FactoryData(process_names)
binVals = Keywords(server, binary_keywords)
#print(binVals.get_keyword())
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)

theme = {
		'dark': False,
		'detail': '#007439',
		'primary': '#00EA64', 
		'secondary': '#6E6E6E'
	}

light_vs_dark = {'Light' : 'indicator-box', 'Dark' : 'indicator-box-dark'}

rootLayout1 = html.Div([
		html.Div(className='indicator-box', id='graph-container', children=[
			html.H4(get_keyword('kbvs', 'prname')),
			dcc.Graph(
				id='production-graph',
				figure=go.Figure({
					'data': [{'x': [], 'y':[]}],
					'layout': go.Layout(
						yaxis=dict(
							title='\'Pressure\' (Torr)',
							range=[0, 0.001],
							tickvals=[0.0000001, 0.0001, 0.001]
						),
						xaxis=dict(title='Time (min)'),
						height=505
					)
				}),
			)
		]),
		html.Div(id='status-container', children=[
			html.Div(className='indicator-box', children=[
				daq.StopButton(id='stop-button')
			]),
			html.Div(className='indicator-box', children=[
				daq.StopButton(id='new-batch', buttonText='Start new batch'),
			]),
			html.Div(className='indicator-box', id='batch-container', children=[
				html.H4("Batch number"),
				daq.LEDDisplay(
					id='batch-number',
					value="124904",
					color='blue'
				),
				html.Div(
					id='batch-started'
				)
			]),
			html.Div(className='indicator-box', id='safety-status', children=[
				html.H4("Safety checks by room"),
				daq.Indicator(
					id='room-one-status',
					value='on',
					color='green',
					label='Materials'
				),
				daq.Indicator(
					id='room-two-status',
					value='on',
					color='orange',
					label='Manufacturing'
				),
				daq.Indicator(
					id='room-three-status',
					value='on',
					color='red',
					label='Packing'
				)
			]),
		]),
		html.Br(),
		html.Div(className='indicator-box', id='cycle-container', children=[
			html.H4('Cycle time (hours)'),
			daq.Gauge(
				id='cycle-time',
				min=0, max=10,
				showCurrentValue=True,
				color={
					"gradient": True,
					"ranges": {
						"green": [0, 6],
						"yellow": [6, 8],
						"red": [8, 10]
					}
				},
			)
		]),
		html.Div(className='indicator-box', id='time-container', children=[
			html.H4('Time to completion (hours)'),
			daq.Gauge(
				id='time-to-completion',
				min=0, max=10,
				showCurrentValue=True,
				color='blue'
			)
		]),
		html.Div(className='indicator-box', id='substance-container', children=[
			html.H4('Substance levels'),
			daq.GraduatedBar(
				id='precursor-levels',
				min=0, max=100,
				step=5,
				color={
						"gradient": True,
						"ranges": {
							"green": [0,35],
							"yellow": [36,65],
							"red": [66,100]
						}
				},
				label='Precursor'
			),
			daq.GraduatedBar(
				id='reagent-levels',
				min=0, max=100,
				step=5,
				color='blue',
				label='Reagent'
			),
			daq.GraduatedBar(
				id='catalyst-levels',
				min=0, max=100,
				step=5,
				color='blue',
				label='Catalyst'
			),
			daq.GraduatedBar(
				id='packaging-levels',
				min=0, max=100,
				step=5,
				color='blue',
				label='Packaging materials'
			)
		]),
		html.Div(className='indicator-box', id='temperature-container', children=[
			html.H4("tmp1"),
			daq.Thermometer(id='manufacturing-temp', 
				min=0, max=273,
				value=100,
				color='blue')
		])
	])

rootLayout2 = html.Div([
		html.Div(id='PWSTATA-container', children=[
			html.Div(className='indicator-box', id='pwstata-status', children=[
				html.H4("Power Bank A"),
				daq.Indicator(
					id='pwa1-status',
					value='on',
					color='green',
					label='Port 1'
				),
				daq.Indicator(
					id='pwa2-status',
					value='on',
					color='green',
					label='Port 2'
				),
				daq.Indicator(
					id='pwa3-status',
					value='on',
					color='green',
					label='Port 3'
				),
				daq.Indicator(
					id='pwa4-status',
					value='on',
					color='green',
					label='Port 4'
				),
				daq.Indicator(
					id='pwa5-status',
					value='on',
					color='green',
					label='Port 5'
				),
				daq.Indicator(
					id='pwa6-status',
					value='on',
					color='green',
					label='Port 6'
				),
				daq.Indicator(
					id='pwa7-status',
					value='on',
					color='green',
					label='Port 7'
				),
				daq.Indicator(
					id='pwa8-status',
					value='on',
					color='green',
					label='Port 8'
				)
			])
		]),
		html.Div(id='PWSTATB-container', children=[
			html.Div(className='indicator-box', id='pwstatb-status', children=[
				html.H4("Power Bank B"),
				daq.Indicator(
					id='pwb1-status',
					value='on',
					color='green',
					label='Port 1'
				),
				daq.Indicator(
					id='pwb2-status',
					value='on',
					color='green',
					label='Port 2'
				),
				daq.Indicator(
					id='pwb3-status',
					value='on',
					color='green',
					label='Port 3'
				),
				daq.Indicator(
					id='pwb4-status',
					value='on',
					color='green',
					label='Port 4'
				),
				daq.Indicator(
					id='pwb5-status',
					value='on',
					color='green',
					label='Port 5'
				),
				daq.Indicator(
					id='pwb6-status',
					value='on',
					color='green',
					label='Port 6'
				),
				daq.Indicator(
					id='pwb7-status',
					value='on',
					color='green',
					label='Port 7'
				),
				daq.Indicator(
					id='pwb8-status',
					value='on',
					color='green',
					label='Port 8'
				)
			])
		]),
		html.Div(id='PWSTATC-container', children=[
			html.Div(className='indicator-box', id='pwstatc-status', children=[
				html.H4("Power Bank C"),
				daq.Indicator(
					id='pwc1-status',
					value='on',
					color='green',
					label='Port 1'
				),
				daq.Indicator(
					id='pwc2-status',
					value='on',
					color='green',
					label='Port 2'
				),
				daq.Indicator(
					id='pwc3-status',
					value='on',
					color='green',
					label='Port 3'
				),
				daq.Indicator(
					id='pwc4-status',
					value='on',
					color='green',
					label='Port 4'
				),
				daq.Indicator(
					id='pwc5-status',
					value='on',
					color='green',
					label='Port 5'
				),
				daq.Indicator(
					id='pwc6-status',
					value='on',
					color='green',
					label='Port 6'
				),
				daq.Indicator(
					id='pwc7-status',
					value='on',
					color='green',
					label='Port 7'
				),
				daq.Indicator(
					id='pwc8-status',
					value='on',
					color='green',
					label='Port 8'
				)
			])
		]),
		html.Div(id='LMP0-container', children=[
			html.Div(className='indicator-box', id='lmp0stat-status', children=[
				html.H4("CAL Lamp 0"),
				daq.Indicator(
					id='lmp0-shutter',
					value='on',
					color='green',
					label='Shutter'
				),
				daq.Indicator(
					id='lmp0-status',
					value='on',
					color='green',
					label='Status'
				)
			])
		]),
		html.Div(id='LMP1-container', children=[
			html.Div(className='indicator-box', id='lmp1stat-status', children=[
				html.H4("CAL Lamp 1"),
				daq.Indicator(
					id='lmp1-shutter',
					value='on',
					color='green',
					label='Shutter'
				),
				daq.Indicator(
					id='lmp1-status',
					value='on',
					color='green',
					label='Status'
				)
			])
		]),
		html.Div(id='LMP2-container', children=[
			html.Div(className='indicator-box', id='lmp2stat-status', children=[
				html.H4("CAL Lamp 2"),
				daq.Indicator(
					id='lmp2-shutter',
					value='on',
					color='green',
					label='Shutter'
				),
				daq.Indicator(
					id='lmp2-status',
					value='on',
					color='green',
					label='Status'
				)
			])
		]),
		html.Div(id='LMP3-container', children=[
			html.Div(className='indicator-box', id='lmp3stat-status', children=[
				html.H4("CAL Lamp 3"),
				daq.Indicator(
					id='lmp3-status',
					value='on',
					color='green',
					label='Status'
				)
			])
		]),
		html.Div(id='BRANGE-container', children=[
			html.Div(className='indicator-box', id='brange-status', children=[
				html.H4("Blue Heater Power Range"),
				daq.Indicator(
					id='br1-status',
					value='on',
					color='green',
					label='Heater 1'
				),
				daq.Indicator(
					id='br2-status',
					value='on',
					color='green',
					label='Heater 2'
				)
			])
		]),
		html.Div(id='RRANGE-container', children=[
			html.Div(className='indicator-box', id='rrange-status', children=[
				html.H4("Red Heater Power Range"),
				daq.Indicator(
					id='rr1-status',
					value='on',
					color='green',
					label='Heater 1'
				),
				daq.Indicator(
					id='rr2-status',
					value='on',
					color='green',
					label='Heater 2'
				)
			])
		]),
		html.Div(id='MISC-container', children=[
			html.Div(className='indicator-box', id='misc-status', children=[
				html.H4("Misc."),
				daq.Indicator(
					id='bfochm-status',
					value='on',
					color='green',
					label='Blue Focus Stage Homed'
				),
				daq.Indicator(
					id='bvhvon-status',
					value='on',
					color='green',
					label='Blue Vac-Ion HV'
				)
			])
		])
])

app.layout = html.Div(id='testing-plotly', children=[
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Factory Data', value='tab-1', children=[
			html.Br(), 
			daq.ToggleSwitch(
				id='daq-light-dark-theme',
				label=['Light', 'Dark'],
				style={'width': '250px', 'margin': 'auto'}, 
				value=False
			),
			html.Br(), 
			html.Div(id='dark-theme-component-demo', 
				children=daq.DarkThemeProvider(theme=theme, children=rootLayout1)),
			dcc.Interval(id='polling-interval',
				n_intervals=0,
				interval=1*1000,
				disabled=True
			),
			dcc.Store(id='annotations-storage',
				data=[]
			)
        ]),
        dcc.Tab(label='On/Off', value='tab-2', children=[ 
			html.Div(id='dark-theme-component-demo2', 
				children=daq.DarkThemeProvider(theme=theme, children=rootLayout2)),
			dcc.Interval(id='polling-interval2',
				n_intervals=0,
				interval=5*1000,
				disabled=False
			),
			dcc.Store(id='annotations-storage2',
				data=[]
			)
        ]),
    ]),
    html.Div(id='tabs-content')
])




@app.callback(
    [Output('polling-interval', 'disabled'),
     Output('stop-button', 'buttonText')],
    [Input('stop-button', 'n_clicks')],
    state=[State('polling-interval', 'disabled')]
)
def stop_production(_, current):
    return not current, "stop" if current else "start"


@app.callback(
    [Output('batch-number', 'value'),
     Output('annotations-storage', 'data'),
     Output('batch-started', 'children')],
    [Input('new-batch', 'n_clicks')],
    state=[State('batch-number', 'value'),
           State('annotations-storage', 'data'),
           State('polling-interval', 'n_intervals'),
           State('production-graph', 'figure')]
)
def new_batch(_, current_batch, current_annotations, n_intervals, current_fig):

    timestamp = datetime.now().strftime('%H:%M:%S %D')

    if len(current_fig['data'][0]['x']) == 0:
        return current_batch, current_annotations, 'Batch started: {}'.format(timestamp)

    marker_x = current_fig['data'][0]['x'][-1]
    marker_y = current_fig['data'][0]['y'][-1]

    current_annotations.append({
        'x': marker_x,
        'y': marker_y,
        'text': 'Batch no. {}'.format(str(int(current_batch) + 1)),
        'arrowhead': 0,
        'bgcolor': 'blue',
        'font': {'color': 'white'}
    })

    return str(int(current_batch) + 1), current_annotations, 'Batch started: {}'.format(timestamp)


@app.callback(
    [Output('cycle-time', 'value'),
     Output('time-to-completion', 'value'),
     Output('room-one-status', 'color'),
     Output('room-two-status', 'color'),
     Output('room-three-status', 'color'),
     Output('precursor-levels', 'value'),
     Output('reagent-levels', 'value'),
     Output('catalyst-levels', 'value'),
     Output('packaging-levels', 'value'),
     Output('production-graph', 'figure'),
     Output('manufacturing-temp', 'value')],
    [Input('polling-interval', 'n_intervals')],
    state=[State('production-graph', 'figure'),
           State('annotations-storage', 'data')]
)
def update_stats(n_intervals, current_fig, current_annotations):

    stats = [fdata.get_data()[pname] for pname in process_names]
    ##print(stats)
    current_data = current_fig['data'][0]
    if n_intervals%30 == 0:
    	new_data = [{'x': current_data['x'].append(n_intervals/60), 
    	'y': current_data['y'].append(get_keyword('kbvs', 'pressure'))}]

    
    #current_fig['layout'].update(annotations=current_annotations)
    #current_fig.update(
    #    figure=go.Figure(
    #        data=new_data
    #    )
    #)

    stats = stats[:-1]
    stats.append(current_fig)
    stats.append(float(get_keyword('kt1s', 'tmp1')))

    return stats

@app.callback(
	[Output('graph-container', 'className'),
	Output('cycle-container', 'className'),
	Output('time-container', 'className'),
	Output('substance-container', 'className'),
	Output('temperature-container', 'className'),
	Output('batch-container', 'className'),
	Output('safety-status', 'className'),
	Output('pwstata-status', 'className'),
	Output('pwstatb-status', 'className'),
	Output('pwstatc-status', 'className'),
	Output('lmp0stat-status', 'className'),
	Output('lmp1stat-status', 'className'),
	Output('lmp2stat-status', 'className'),
	Output('lmp3stat-status', 'className'),
	Output('brange-status', 'className'),
	Output('rrange-status', 'className'),
	Output('misc-status', 'className')],
	[Input('daq-light-dark-theme', 'value')]
)
def change_class_name(dark_theme):
	bVw = list()
	temp = ''
	if(dark_theme):
		temp = '-dark'
	for x in range(0,17):
		bVw.append('indicator-box'+temp)
	
	return bVw

@app.callback(
    Output('dark-theme-component-demo', 'children'),
    [Input('daq-light-dark-theme', 'value')]
)
def turn_dark(dark_theme): 
    if(dark_theme):
        theme.update(
            dark=True
        )
        lvd = 'Dark'
    else:
        theme.update(
            dark=False
        )
        lvd = 'Light'
    return daq.DarkThemeProvider(theme=theme, children=rootLayout1)


@app.callback(
    Output('testing-plotly', 'style'),
    [Input('daq-light-dark-theme', 'value')]
)
def change_bg(dark_theme):
	if(dark_theme):
		return {'background-color': '#303030', 'color': 'white'}
	else:
		return {'background-color': 'white', 'color': 'black'}

@app.callback(
	[Output('pwa1-status', 'color'),
	Output('pwa2-status', 'color'),
	Output('pwa3-status', 'color'),
	Output('pwa4-status', 'color'),
	Output('pwa5-status', 'color'),
	Output('pwa6-status', 'color'),
	Output('pwa7-status', 'color'),
	Output('pwa8-status', 'color'),
	Output('pwb1-status', 'color'),
	Output('pwb2-status', 'color'),
	Output('pwb3-status', 'color'),
	Output('pwb4-status', 'color'),
	Output('pwb5-status', 'color'),
	Output('pwb6-status', 'color'),
	Output('pwb7-status', 'color'),
	Output('pwb8-status', 'color'),
	Output('pwc1-status', 'color'),
	Output('pwc2-status', 'color'),
	Output('pwc3-status', 'color'),
	Output('pwc4-status', 'color'),
	Output('pwc5-status', 'color'),
	Output('pwc6-status', 'color'),
	Output('pwc7-status', 'color'),
	Output('pwc8-status', 'color'),
	Output('pwa1-status', 'label'),
	Output('pwa2-status', 'label'),
	Output('pwa3-status', 'label'),
	Output('pwa4-status', 'label'),
	Output('pwa5-status', 'label'),
	Output('pwa6-status', 'label'),
	Output('pwa7-status', 'label'),
	Output('pwa8-status', 'label'),
	Output('pwb1-status', 'label'),
	Output('pwb2-status', 'label'),
	Output('pwb3-status', 'label'),
	Output('pwb4-status', 'label'),
	Output('pwb5-status', 'label'),
	Output('pwb6-status', 'label'),
	Output('pwb7-status', 'label'),
	Output('pwb8-status', 'label'),
	Output('pwc1-status', 'label'),
	Output('pwc2-status', 'label'),
	Output('pwc3-status', 'label'),
	Output('pwc4-status', 'label'),
	Output('pwc5-status', 'label'),
	Output('pwc6-status', 'label'),
	Output('pwc7-status', 'label'),
	Output('pwc8-status', 'label')],
	[Input('polling-interval2', 'n_intervals')],
	state=[State('tabs', 'children'),
	State('annotations-storage2', 'data')]
)
def update(n_intervals, tab, current_annotations):
	newBinVal = binVals.get_keyword()
	stats = [newBinVal[keyword] for keyword in binary_keywords]
	#print(stats)
	color_list = []
	counter = 0
	for val in stats:
		if binary_keywords[counter][1:6] == 'RANGE':
			if val == '0':
				color_list.append('red')
			elif val == '1':
				color_list.append('yellow')
			else:
				color_list.append('green')
		else:
			if val == '0':
				color_list.append('red')
			elif val == '1':
				color_list.append('green')
			else:
				color_list.append(val)
		counter = counter + 1
	return color_list



if __name__ == '__main__':
    app.run_server(debug=True)
