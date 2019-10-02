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
for i in range(0,13):
	binary_keywords.append('uptime')
binary_keywords.append('TESTINT1')
for i in ['A','B','C']:
	for j in range(1,9):
		binary_keywords.append('PWSTAT'+str(j)+i)
	for j in range(1,9):
		binary_keywords.append('PWNAME'+str(j)+i)
#for i in range(0,3):
#	binary_keywords.append('LMP'+str(i)+'SHST')
#	binary_keywords.append('LMP'+str(i)+'STAT')
#binary_keywords.append('LMP3STAT')
#for i in ['BRANGE', 'RRANGE']:
#	for j in range(1,3):
#		binary_keywords.append(i+str(j))
#binary_keywords.append('BROCHM')
#binary_keywords.append('BVHVON')

binary_keywords[0] = binary_keywords[0] +'kt1s'
binary_keywords[1] = binary_keywords[1] +'kt2s'
binary_keywords[2] = binary_keywords[2] +'kp1s'
binary_keywords[3] = binary_keywords[3] +'kp2s'
binary_keywords[4] = binary_keywords[4] +'kp3s'
binary_keywords[5] = binary_keywords[5] +'kbgs'
binary_keywords[6] = binary_keywords[6] +'kbvs'
binary_keywords[7] = binary_keywords[7] +'kbds'
binary_keywords[8] = binary_keywords[8] +'kfcs'
binary_keywords[9] = binary_keywords[9] +'kbes'
binary_keywords[10] = binary_keywords[10] +'kbms'
binary_keywords[11] = binary_keywords[11] +'kros'
binary_keywords[12] = binary_keywords[12] +'kcas'

allServers = ['kt1s',
'kt2s',
'kp1s',
'kp2s',
'kp3s',
'kbgs',
'kbvs',
'kbds',
'kfcs',
'kbes',
'kbms',
'kros',
'kcas',
'kcwi']

server = []
for i in allServers:
	server.append(i)

for i in range(1,4):
	for j in range(1,17):
		server.append('kp'+str(i)+'s')


#print(server)
#print(binary_keywords)
fdata = FactoryData(process_names)
binVals = Keywords(server, binary_keywords)
histKeys = Keywords()
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


rootLayout = html.Div([
		html.Div(id='SERVER-container', children=[
			html.H1("All Servers"),
			html.Div(className='indicator-box', id='temperature-servers', children=[
				html.H4('Temperature'),
				daq.Indicator(
					id='kt1s-status',
					value=True,
					color='blue',
					label='kt1s'
				),
				daq.Indicator(
					id='kt2s-status',
					value=True,
					color='blue',
					label='kt2s'
				)
			]),
			html.Div(className='indicator-box', id='power-servers', children=[
				html.H4("Power"),
				daq.Indicator(
					id='kp1s-status',
					value=True,
					color='blue',
					label='kp1s'
				),
				daq.Indicator(
					id='kp2s-status',
					value=True,
					color='blue',
					label='kp2s'
				),
				daq.Indicator(
					id='kp3s-status',
					value=True,
					color='blue',
					label='kp3s'
				)
			]),
			html.Div(className='indicator-box', id='pressure-servers', children=[
				html.H4("Pressure"),
				daq.Indicator(
					id='kbgs-status',
					value=True,
					color='blue',
					label='kbgs'
				),
				daq.Indicator(
					id='kbvs-status',
					value=True,
					color='blue',
					label='kbvs'
				)
			]),
			html.Div(className='indicator-box', id='detector-servers', children=[
				html.H4("Detector"),
				daq.Indicator(
					id='kbds-status',
					value=True,
					color='blue',
					label='kbds'
				),
				daq.Indicator(
					id='kfcs-status',
					value=True,
					color='blue',
					label='kfcs'
				)
			]),
			html.Div(className='indicator-box', id='mechanism-servers', children=[
				html.H4("Mechanisms"),
				daq.Indicator(
					id='kbes-status',
					value=True,
					color='blue',
					label='kbes'
				),
				daq.Indicator(
					id='kbms-status',
					value=True,
					color='blue',
					label='kbms'
				),
				daq.Indicator(
					id='kros-status',
					value=True,
					color='blue',
					label='kros'
				),
				daq.Indicator(
					id='kcas-status',
					value=True,
					color='blue',
					label='kcas'
				)
			]),
			html.Div(className='indicator-box', id='global-servers', children=[
				html.H4("Global"),
				daq.Indicator(
					id='kcwi-status',
					value=True,
					color='blue',
					label='kcwi'
				)
			])
		])
])

rootLayout1 = html.Div([
		html.Div(id='status-container', children=[
			html.Div(className='indicator-box', children=[
				daq.StopButton(id='stop-button')
			]),
			html.Div(className='indicator-box', id='server-status', children=[
				html.H4("Legend"),
				daq.Indicator(
					id='legend-green',
					value=True,
					color='green',
					label='OK ='
				),
				daq.Indicator(
					id='legend-yellow',
					value=True,
					color='yellow',
					label='Off, but Operational ='
				),
				daq.Indicator(
					id='legend-red',
					value=True,
					color='red',
					label='Off/Do Not Run ='
				)
			])
		]),
		html.Br(),
		html.Div(className='indicator-box', id='pgpress-container', children=[
			html.H4('Blue Pressure Gauge'),
			daq.Gauge(
				id='pgpress-status',
				min=0, max=1,
				showCurrentValue=True,
				color={
					"gradient": True,
					"ranges": {
						"green": [0, 0.3],
						"yellow": [0.3, 0.7],
						"red": [0.7, 1]
					}
				},
			),
			html.P('Order of 1000')
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



temperatureRoot2 = html.Div()

powerRoot2 = html.Div([
	html.Div(id='PWSTATA-container', children=[
			html.Div(className='indicator-box', id='pwstata-status', children=[
				html.H4("Power Bank A"),
				daq.Indicator(
					id='pwa1-status',
					value=True,
					color='green',
					label='Port 1'
				),
				daq.Indicator(
					id='pwa2-status',
					value=True,
					color='green',
					label='Port 2'
				),
				daq.Indicator(
					id='pwa3-status',
					value=True,
					color='green',
					label='Port 3'
				),
				daq.Indicator(
					id='pwa4-status',
					value=True,
					color='green',
					label='Port 4'
				),
				daq.Indicator(
					id='pwa5-status',
					value=True,
					color='green',
					label='Port 5'
				),
				daq.Indicator(
					id='pwa6-status',
					value=True,
					color='green',
					label='Port 6'
				),
				daq.Indicator(
					id='pwa7-status',
					value=True,
					color='green',
					label='Port 7'
				),
				daq.Indicator(
					id='pwa8-status',
					value=True,
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
				value=True,
				color='green',
				label='Port 1'
			),
			daq.Indicator(
				id='pwb2-status',
				value=True,
				color='green',
				label='Port 2'
			),
			daq.Indicator(
				id='pwb3-status',
				value=True,
				color='green',
				label='Port 3'
			),
			daq.Indicator(
				id='pwb4-status',
				value=True,
				color='green',
				label='Port 4'
			),
			daq.Indicator(
				id='pwb5-status',
				value=True,
				color='green',
				label='Port 5'
			),
			daq.Indicator(
				id='pwb6-status',
				value=True,
				color='green',
				label='Port 6'
			),
			daq.Indicator(
				id='pwb7-status',
				value=True,
				color='green',
				label='Port 7'
			),
			daq.Indicator(
				id='pwb8-status',
				value=True,
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
				value=True,
				color='green',
				label='Port 1'
			),
			daq.Indicator(
				id='pwc2-status',
				value=True,
				color='green',
				label='Port 2'
			),
			daq.Indicator(
				id='pwc3-status',
				value=True,
				color='green',
				label='Port 3'
			),
			daq.Indicator(
				id='pwc4-status',
				value=True,
				color='green',
				label='Port 4'
			),
			daq.Indicator(
				id='pwc5-status',
				value=True,
				color='green',
				label='Port 5'
			),
			daq.Indicator(
				id='pwc6-status',
				value=True,
				color='green',
				label='Port 6'
			),
			daq.Indicator(
				id='pwc7-status',
				value=True,
				color='green',
				label='Port 7'
			),
			daq.Indicator(
				id='pwc8-status',
				value=True,
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
				value=True,
				color='green',
				label='Shutter'
			),
			daq.Indicator(
				id='lmp0-status',
				value=True,
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
				value=True,
				color='green',
				label='Shutter'
			),
			daq.Indicator(
				id='lmp1-status',
				value=True,
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
				value=True,
				color='green',
				label='Shutter'
			),
			daq.Indicator(
				id='lmp2-status',
				value=True,
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
				value=True,
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
				value=True,
				color='green',
				label='Heater 1'
			),
			daq.Indicator(
				id='br2-status',
				value=True,
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
				value=True,
				color='green',
				label='Heater 1'
			),
			daq.Indicator(
				id='rr2-status',
				value=True,
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
				value=True,
				color='green',
				label='Blue Focus Stage Homed'
			),
			daq.Indicator(
				id='bvhvon-status',
				value=True,
				color='green',
				label='Blue Vac-Ion HV'
			)
		])
	])
])

layout_dark = go.Layout(
    yaxis=dict(
        title='\'Pressure\' (Torr)',
        range=[0, 0.001],
        tickvals=[0.0000001, 0.0001, 0.001],
        tickfont= {'color':'#FFFFFF'},
        color='white'
    ),
    xaxis=dict(
        title='Time (min)',
        tickfont= {'color':'#FFFFFF'},
        color='white'
    ),
    height=505,
    plot_bgcolor="#313336",
    paper_bgcolor="#303030"
)
layout = go.Layout(
    yaxis=dict(
        title='\'Pressure\' (Torr)',
        range=[0, 0.001],
        tickvals=[0.0000001, 0.0001, 0.001]
    ),
    xaxis=dict(
        title='Time (min)'
    ),
    height=505,
    plot_bgcolor="#f3f3f3"
)

pressureRoot2 = html.Div([
    html.Div(className='indicator-box', id='graph-container', children=[
        html.H4(get_keyword('kbvs', 'prname')),
        dcc.Graph(
            id='production-graph',
            figure=go.Figure({
                'data': [{'x': [], 'y':[]}],
                'layout': layout
            }),
        )
    ]),
    html.Div(id='status-container1', children=[
        html.Div(className='indicator-box', id='dropdown-container', children=[
            html.H4('Pressure History'),
            html.Div(className='dropdown-theme', id='dropdown', children=[
                dcc.Dropdown(
                    id='graph-dropdown',
                    options=[
                        {'label': '1 Day Ago', 'value': 'day'},
                        {'label': '1 Week Ago', 'value': 'week'},
                        {'label': '1 Month Ago', 'value': 'month'},
                        {'label': 'None', 'value': 'fake'}
                    ],
                    value='fake',
                    style=theme
                )
            ])
        ])
    ])
])

detectorRoot2 = html.Div()

mechanismsRoot2 = html.Div()



page1 = [
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(id='tab1', label='Factory Data', value='tabs1', className='custom-tab',
                selected_className='custom-tab--selected', children=[
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
        dcc.Tab(id='tab2', label='All Servers', value='tab2', className='custom-tab',
                selected_className='custom-tab--selected', children=[
			html.Div(id='dark-theme-component-demo2',
				children=daq.DarkThemeProvider(theme=theme, children=[
					dcc.Tabs(id='subtabs', value='subtabs1', children=[
						dcc.Tab(id='subtab1', label='Temperature Servers', value='subtab1',className='custom-tab',
                			selected_className='custom-tab--selected', children=temperatureRoot2),
						dcc.Tab(id='subtab2', label='Power Servers', value='subtab2', className='custom-tab',
                			selected_className='custom-tab--selected', children=powerRoot2),
						dcc.Tab(id='subtab3', label='Pressure Servers', value='subtab3', className='custom-tab',
                			selected_className='custom-tab--selected', children=pressureRoot2),
						dcc.Tab(id='subtab4', label='Detector Servers', value='subtab4', className='custom-tab',
                			selected_className='custom-tab--selected', children=detectorRoot2),
						dcc.Tab(id='subtab5', label='Mechanisms Servers', value='subtab5', className='custom-tab',
                			selected_className='custom-tab--selected', children=mechanismsRoot2)
					]),
					rootLayout
				])),
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
]

app.layout = html.Div(id='testing-plotly', children=page1)



@app.callback(
    [Output('polling-interval', 'disabled'),
     Output('stop-button', 'buttonText')],
    [Input('stop-button', 'n_clicks')],
    state=[State('polling-interval', 'disabled')]
)
def stop_production(_, current):
    return not current, "stop" if current else "start"


@app.callback(
	[Output('graph-container', 'className'),
	Output('pgpress-container', 'className'),
	Output('time-container', 'className'),
	Output('substance-container', 'className'),
	Output('temperature-container', 'className'),
	Output('server-status', 'className'),
	Output('pwstata-status', 'className'),
	Output('pwstatb-status', 'className'),
	Output('pwstatc-status', 'className'),
	Output('lmp0stat-status', 'className'),
	Output('lmp1stat-status', 'className'),
	Output('lmp2stat-status', 'className'),
	Output('lmp3stat-status', 'className'),
	Output('brange-status', 'className'),
	Output('rrange-status', 'className'),
	Output('misc-status', 'className'),
	Output('temperature-servers', 'className'),
	Output('power-servers', 'className'),
	Output('pressure-servers', 'className'),
	Output('detector-servers', 'className'),
	Output('mechanism-servers', 'className'),
	Output('global-servers', 'className'),
    Output('dropdown-container', 'className'),
    Output('dropdown', 'className'),
    Output('production-graph', 'figure')],
	[Input('daq-light-dark-theme', 'value'),
    Input('graph-dropdown', 'value')],
    state=[State('production-graph', 'figure')]
)
def change_class_name(dark_theme, value, current_fig):
    bVw = list()
    temp = ''
    current_fig['layout'] = layout
    if(dark_theme):
        temp = '-dark'
        current_fig['layout'] = layout_dark
    for x in range(0,23):
        bVw.append('indicator-box'+temp)
    bVw.append('dropdown-theme'+temp)

    current_data = current_fig['data'][0]
    new_data = [histKeys.get_keyword_history('kbvs', 'pressure', value)]
    current_fig['data'] = new_data
    bVw.append(current_fig)
    return bVw


@app.callback(
	[Output('tab1', 'className'),
	 Output('tab1', 'selected_className'),
	 Output('tab2', 'className'),
	 Output('tab2', 'selected_className'),
	 Output('subtab1', 'className'),
	 Output('subtab1', 'selected_className'),
	 Output('subtab2', 'className'),
	 Output('subtab2', 'selected_className'),
	 Output('subtab3', 'className'),
	 Output('subtab3', 'selected_className'),
	 Output('subtab4', 'className'),
	 Output('subtab4', 'selected_className'),
	 Output('subtab5', 'className'),
	 Output('subtab5', 'selected_className')],
	[Input('daq-light-dark-theme', 'value')]
)
def change_class_name_tab(dark_theme):
	bVw = list()
	temp = ''
	if(dark_theme):
		temp = '-dark'
	for x in range(0,7):
		bVw.append('custom-tab'+temp)
		bVw.append('custom-tab--selected'+temp)

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
    [Output('pgpress-status', 'value'),
     Output('time-to-completion', 'value'),
     Output('precursor-levels', 'value'),
     Output('reagent-levels', 'value'),
     Output('catalyst-levels', 'value'),
     Output('packaging-levels', 'value'),
     Output('manufacturing-temp', 'value')],
    [Input('polling-interval', 'n_intervals')]
)
def update_stats(n_intervals):

    stats = [fdata.get_data()[pname] for pname in process_names]
    stats[0] = float(get_keyword('kbgs', 'pgpress'))*10**3
    # current_data = current_fig['data'][0]
    # if n_intervals%30 == 0:
    # 	new_data = [{'x': current_data['x'].append(n_intervals/60),
    # 	'y': current_data['y'].append(get_keyword('kbvs', 'pressure'))}]
    #
    #
    # #current_fig['layout'].update(annotations=current_annotations)
    # #current_fig.update(
    # #    figure=go.Figure(
    # #        data=new_data
    # #    )
    # #)
    #
    stats = stats[:-1]
    # stats.append(current_fig)
    stats.append(float(get_keyword('kt1s', 'tmp1')))

    return stats

@app.callback(
	[Output('kt1s-status', 'color'),
	Output('kt2s-status', 'color'),
	Output('kp1s-status', 'color'),
	Output('kp2s-status', 'color'),
	Output('kp3s-status', 'color'),
	Output('kbgs-status', 'color'),
	Output('kbvs-status', 'color'),
	Output('kbds-status', 'color'),
	Output('kfcs-status', 'color'),
	Output('kbes-status', 'color'),
	Output('kbms-status', 'color'),
	Output('kros-status', 'color'),
	Output('kcas-status', 'color'),
	Output('kcwi-status', 'color'),
	Output('pwa1-status', 'color'),
	Output('pwa2-status', 'color'),
	Output('pwa3-status', 'color'),
	Output('pwa4-status', 'color'),
	Output('pwa5-status', 'color'),
	Output('pwa6-status', 'color'),
	Output('pwa7-status', 'color'),
	Output('pwa8-status', 'color'),
	Output('pwa1-status', 'label'),
	Output('pwa2-status', 'label'),
	Output('pwa3-status', 'label'),
	Output('pwa4-status', 'label'),
	Output('pwa5-status', 'label'),
	Output('pwa6-status', 'label'),
	Output('pwa7-status', 'label'),
	Output('pwa8-status', 'label'),
	Output('pwb1-status', 'color'),
	Output('pwb2-status', 'color'),
	Output('pwb3-status', 'color'),
	Output('pwb4-status', 'color'),
	Output('pwb5-status', 'color'),
	Output('pwb6-status', 'color'),
	Output('pwb7-status', 'color'),
	Output('pwb8-status', 'color'),
	Output('pwb1-status', 'label'),
	Output('pwb2-status', 'label'),
	Output('pwb3-status', 'label'),
	Output('pwb4-status', 'label'),
	Output('pwb5-status', 'label'),
	Output('pwb6-status', 'label'),
	Output('pwb7-status', 'label'),
	Output('pwb8-status', 'label'),
	Output('pwc1-status', 'color'),
	Output('pwc2-status', 'color'),
	Output('pwc3-status', 'color'),
	Output('pwc4-status', 'color'),
	Output('pwc5-status', 'color'),
	Output('pwc6-status', 'color'),
	Output('pwc7-status', 'color'),
	Output('pwc8-status', 'color'),
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
	#print(newBinVal)
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
