# https://www.statworx.com/at/blog/how-to-build-a-dashboard-in-python-plotly-dash-step-by-step-tutorial/
# https://dash.plotly.com/deployment
import os
import plotly.graph_objects as go
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Load data
df = pd.read_csv('data/stockdata2.csv', index_col=0, parse_dates=True)
df.index = pd.to_datetime(df['Date'])

app = dash.Dash(__name__)

server = app.server

# use pandas dataframe
filename = "Form6.txt"
df2 = pd.read_table(filename, delimiter=r"|")

# create header and row list
header = []
with open(file="header.txt") as myFile4:
    for num, line in enumerate(myFile4, 1):
        x = line.rstrip()
        header.append(x)

row = []
with open(file="row.txt") as myFile5:
    for num, line in enumerate(myFile5, 1):
        x = line.rstrip()
        row.append(x)

# clean up data
df2 = df2.replace("MSIG INSURANCE (SINGAPORE) PTE. LTD.", "MSIG")
df2 = df2.replace("NTUC INCOME INSURANCE CO-OPERATIVE LIMITED", "NTUC Income")
df2 = df2.replace(dict.fromkeys(["FIRST CAPITAL INSURANCE LTD",
                                 "MS FIRST CAPITAL INSURANCE LIMITED"], "MS First Capital"))
df2 = df2.replace("ZURICH INSURANCE COMPANY LTD (SINGAPORE BRANCH)", "Zurich")
df2 = df2.replace(dict.fromkeys(["AMERICAN HOME ASSURANCE CO",
                                 "CHARTIS SINGAPORE INSURANCE PTE. LTD.",
                                 "AIG ASIA PACIFIC INSURANCE PTE. LTD."], "AIG"))
df2 = df2.replace(dict.fromkeys(["SHC CAPITAL LIMITED",
                                 "SHC INSURANCE PTE. LTD.",
                                 "ERGO INSURANCE PTE. LTD."], "ERGO"))
df2 = df2.replace(dict.fromkeys(["AXA INSURANCE SINGAPORE PTE LTD",
                                 "AXA INSURANCE PTE LTD",
                                 "RED SWITCH PTE LTD"], "AXA"))
df2.drop_duplicates(subset=('year', 'Row No.', 'insurer_name'), inplace=True, keep=False)  # remove multiple headers
df2[header] = df2[header].astype(str).astype(float)  # convert string to float
df2.reset_index(drop=True, inplace=True)
df2.to_csv(r'test.txt', sep='|')
unique = df2.insurer_name.unique()
years = df2.year.unique()


# Creates a list of dictionaries, which have the keys 'label' and 'value'.
def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list


app.layout = html.Div(children=[
    html.Div(className='row',  # Define the row element
             children=[
                 html.Div(className='three columns div-user-controls',
                          children=[
                              html.H2('General Insurers in Singapore'),
                              html.P('''Visualising MAS Form 6'''),
                              html.P('''Pick one or more insurer below.'''),
                              html.Div(className='div-for-dropdown',
                                       children=[
                                           dcc.Dropdown(id='insurerselector',
                                                        options=get_options(df2['insurer_name'].unique()),
                                                        multi=True,
                                                        value=[df2['insurer_name'].sort_values()[0]],
                                                        style={'backgroundColor': '#ffffff'},
                                                        className='insurerselector')
                                       ],
                                       style={'color': '#1E1E1E'})
                          ]
                          ),  # Define the left element
                 html.Div(className='nine columns div-for-charts bg-grey',
                          children=[dcc.Graph(id='timeseries', config={'displayModeBar': False})]
                          )  # Define the right element
             ]
             )
])


@app.callback(Output('timeseries', 'figure'),
              [Input('insurerselector', 'value')])
def update_timeseries(selected_dropdown_value):
    ''' Draw traces of the feature 'value' based one the currently selected stocks '''
    # STEP 1
    trace = []
    # STEP 2
    # Draw and append traces for each stock
    for insurer in selected_dropdown_value:
        df_nlr = df2[(df2.insurer_name == insurer) & (df2.Description == "Net Loss Ratio")]
        for i in header[1:]:
            trace.append(go.Scatter(x=df_nlr['year'].tolist(),
                                    y=df_nlr[i].tolist(),
                                    opacity=0.7,
                                    name=i,
                                    legendgroup=i,
                                    textposition='bottom center'))
    # STEP 3
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # STEP 4
    figure = {'data': data,
              'layout': go.Layout(
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  height=700,
                  autosize=True,
                  title={'text': 'Net Loss Ratio', 'font': {'color': 'black'}, 'x': 0.5},
                  yaxis={'range': [0, 1.6]},
              ),

              }

    return figure


# @app.callback(Output('change', 'figure'),
#               [Input('insurerselector', 'value')])
# def update_change(selected_dropdown_value):
#     ''' Draw traces of the feature 'change' based one the currently selected stocks '''
#     trace = []
#     df_sub = df
#     # Draw and append traces for each stock
#     for stock in selected_dropdown_value:
#         trace.append(go.Scatter(x=df_sub[df_sub['stock'] == stock].index,
#                                 y=df_sub[df_sub['stock'] == stock]['change'],
#                                 mode='lines',
#                                 opacity=0.7,
#                                 name=stock,
#                                 textposition='bottom center'))
#     traces = [trace]
#     data = [val for sublist in traces for val in sublist]
#     # Define Figure
#     figure = {'data': data,
#               'layout': go.Layout(
#                   paper_bgcolor='rgba(0, 0, 0, 0)',
#                   plot_bgcolor='rgba(0, 0, 0, 0)',
#                   margin={'t': 50},
#                   height=250,
#                   hovermode='x',
#                   autosize=True,
#                   title={'text': 'Daily Change', 'font': {'color': 'black'}, 'x': 0.5},
#                   xaxis={'showticklabels': False, 'range': [df_sub.index.min(), df_sub.index.max()]},
#               ),
#               }
#
#     return figure


if __name__ == '__main__':
    app.run_server(debug=True)
