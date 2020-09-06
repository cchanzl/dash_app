# https://www.statworx.com/at/blog/how-to-build-a-dashboard-in-python-plotly-dash-step-by-step-tutorial/
# https://dash.plotly.com/deployment
import os
import plotly.graph_objects as go
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

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
df2 = df2.replace("DIRECT ASIA INSURANCE (SINGAPORE) PTE LTD", "Direct Asia")
df2 = df2.replace("INDIA INTERNATIONAL INSURANCE PTE LTD", "India International")
df2 = df2.replace("NTUC INCOME INSURANCE CO-OPERATIVE LIMITED", "NTUC Income")
df2 = df2.replace("TOKIO MARINE INSURANCE SINGAPORE LTD", "Tokio Marine")
df2 = df2.replace("ZURICH INSURANCE COMPANY LTD (SINGAPORE BRANCH)", "Zurich")
df2 = df2.replace(dict.fromkeys(["SHC CAPITAL LIMITED", "SHC INSURANCE PTE. LTD.", "ERGO INSURANCE PTE. LTD."], "ERGO"))

df2 = df2.replace(dict.fromkeys(["FIRST CAPITAL INSURANCE LTD",
                                 "MS FIRST CAPITAL INSURANCE LIMITED"], "MS First Capital"))

df2 = df2.replace(dict.fromkeys(["ATRADIUS CREDIT INSURANCE N.V., SINGAPORE BRANCH",
                                 "ATRADIUS CREDITO Y CAUCION S.A. DE SEGUROS Y REASE"], "Atradius"))

df2 = df2.replace(dict.fromkeys(["CIGNA EUROPE INSURANCE CO S.A.-N.V., SPORE BRANCH",
                                 "CIGNA EUROPE INSURANCE CO S.A.-N.V., SG BRANCH",
                                 "CIGNA EUROPE INSURANCE CO S.A.-N.V., SINGAPORE BRANCH"], "Cigna"))

df2 = df2.replace(dict.fromkeys(["AMERICAN HOME ASSURANCE CO", "CHARTIS SINGAPORE INSURANCE PTE. LTD.",
                                 "AIG ASIA PACIFIC INSURANCE PTE. LTD."], "AIG"))

df2 = df2.replace(dict.fromkeys(["AXA INSURANCE SINGAPORE PTE LTD", "AXA INSURANCE PTE LTD",
                                 "RED SWITCH PTE LTD"], "AXA"))

df2 = df2.replace(dict.fromkeys(["SOMPO JAPAN INSURANCE (SINGAPORE) PTE. LTD.", "TENET SOMPO INSURANCE PTE. LTD.",
                                 "SOMPO INSURANCE SINGAPORE PTE. LTD."], "Sompo"))

df2 = df2.replace(dict.fromkeys(["QBE INSURANCE INTERNATIONAL LTD", "QBE INSURANCE INTERNATIONAL LTD, SINGAPORE BRANCH",
                                 "QBE INSURANCE (INTERNATIONAL) LTD, SINGAPORE BRANCH",
                                 "QBE INSURANCE (SINGAPORE) PTE. LTD."], "QBE"))

df2.drop_duplicates(subset=('year', 'Row No.', 'insurer_name'), inplace=True, keep=False)  # remove multiple headers
df2[header] = df2[header].astype(str).astype(float)  # convert string to float
df2.reset_index(drop=True, inplace=True)
df2.to_csv(r'test.txt', sep='|')
unique = sorted(list(df2.insurer_name.unique()))
years = df2.year.unique()


# Creates a list of dictionaries, which have the keys 'label' and 'value'.
def get_options(list_lob):
    dict_list = []
    for i in list_lob:
        dict_list.append({'label': i, 'value': i})

    return dict_list


app.layout = html.Div(children=[
    html.Div(className='row',  # row 1
             children=[
                 html.Div(className='nine columns div-user-controls',
                          children=[
                              # html.H2('Net Loss Ratios of General Insurers in Singapore'),
                              # html.P('''Data source: MAS Insurer Returns - Form 6''')
                          ]
                          ),
             ]
             ),

    html.Div(className='row',  # row 2 of checkboxes
             children=[
                 html.Div(className='five columns div-user-controls',
                          children=[
                              html.P('''Pick one or more lines of business below.'''),
                              html.Div(className='div-for-checklist',
                                       children=[
                                           dcc.Checklist(
                                               id='lobselector',
                                               options=get_options(header[1:]),
                                               value=[header[1:][3]],
                                               className='lobselector',
                                               labelStyle={'display': 'block'}
                                           ),
                                       ],
                                       style={'color': '#1E1E1E'}),
                          ]
                          ),
                 html.Div(className='five columns div-user-controls',
                          children=[
                              html.P('''Pick one or more insurers below.'''),
                              html.Div(className='div-for-checklist',
                                       children=[
                                           dcc.Checklist(
                                               id='insurerselector',
                                               options=get_options(unique),
                                               value=list(unique[0:len(unique)]),  # select all insurers from start
                                               className='insurerselector',
                                               labelStyle={'display': 'block'}
                                           ),
                                       ],
                                       style={'color': '#1E1E1E'}),
                          ])
             ]),
    html.Div(className='row',  # Define the row element
             children=[
                 html.Div(className='nine columns div-user-controls',
                          children=[
                              html.H2('Net Written Premium of General Insurers in Singapore'),
                              html.P('''Net of reinsurance cessions'''),
                              dcc.Graph(id='nwp_bar', config={'displayModeBar': False}),
                              html.H2('Net Loss Ratios of General Insurers in Singapore'),
                              html.P('''Net Loss Ratio = Net Claims Settled / Net Written Premium'''),
                              dcc.Graph(id='lossratio_line', config={'displayModeBar': False}),
                          ]
                          ),  # Define the left element
             ]),
    html.Div(className='row',  # Define the row element
             children=[
                 html.Div(className='eight columns div-user-controls',
                          children=[
                              dcc.Graph(id='lossratio_box', config={'displayModeBar': False}),

                              html.H2('Combined Operating Ratios of General Insurers in Singapore'),
                              html.P('''Combined Operating Ratio = (Net Claims Settled + Mgmt. Expenses + Net 
                          Commissions) / Net Written Premium'''),
                              dcc.Graph(id='cor_box', config={'displayModeBar': False}),
                          ]
                          ),  # Define the left element
             ]),

])


# # Graph 1 - Net Written Premium - Bar
@app.callback(Output('nwp_bar', 'figure'),
              [Input('lobselector', 'value'), Input('insurerselector', 'value')])
def update_lossratio(lobselector, insurerselector):
    # STEP 1
    trace = []
    # STEP 2
    # Draw and append traces for each stock
    for lob in lobselector:
        df_nwp = df2[['year', 'insurer_name', 'Description', lob]]
        df_nwp = df_nwp[df_nwp.Description == 'Net premiums written']
        for i in insurerselector:
            df_nwp_i = df_nwp[df_nwp.insurer_name == i]
            df_nwp_i = df_nwp_i[df_nwp[lob] != 0]  # remove data where there is 0 loss ratio
            trace.append(go.Bar(x=years,
                                y=df_nwp_i[lob].tolist(),
                                opacity=0.7,
                                name=i + " - " + lob,
                                legendgroup=i,
                                text=df_nwp_i['insurer_name'] + " - " + lob,
                                hovertemplate=
                                "<b>%{text}</b><br>" +
                                "Year: %{x:.f}<br>" +
                                "NLR: %{y:.0%}<br>" +
                                "<extra></extra>",
                                ))
    # STEP 3
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # STEP 4
    figure = {'data': data,
              'layout': go.Layout(
                  barmode='stack',
                  margin=dict(b=40, t=10),  # l, r, b, t
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  hovermode='closest',
                  showlegend=True,
                  height=400,
                  autosize=True,
                  # title={'text': 'Net Loss Ratio', 'font': {'color': 'black'}, 'x': 0.5},
                  yaxis=dict(
                      title='Net Written Premiums (SGD)',
                      tickformat=".3s",
                      titlefont=dict(
                          family='Arial',
                          size=15,
                          color='lightgrey')
                  ),
                  xaxis=dict(
                      title='Reporting Year',
                      titlefont=dict(
                          family='Arial',
                          size=15,
                          color='lightgrey')
                  ),
              ),
              }

    return figure


# Graph 2 - Net Loss Ratio - Line
@app.callback(Output('lossratio_line', 'figure'),
              [Input('lobselector', 'value'), Input('insurerselector', 'value')])
def update_lossratio(lobselector, insurerselector):
    # STEP 1
    trace = []
    # STEP 2
    # Draw and append traces for each stock
    for lob in lobselector:
        df_nlr = df2[['year', 'insurer_name', 'Description', lob]]
        df_nlr = df_nlr[df_nlr.Description == 'Net Loss Ratio']
        for i in insurerselector:
            df_nlr_i = df_nlr[df_nlr.insurer_name == i]
            df_nlr_i = df_nlr_i[df_nlr[lob] != 0]  # remove data where there is 0 loss ratio
            trace.append(go.Scatter(x=df_nlr_i['year'].tolist(),
                                    y=df_nlr_i[lob].tolist(),
                                    opacity=0.7,
                                    name=i + " - " + lob,
                                    legendgroup=i,
                                    textposition='bottom center',
                                    text=df_nlr_i['insurer_name'] + " - " + lob,
                                    hovertemplate=
                                    "<b>%{text}</b><br>" +
                                    "Year: %{x:.f}<br>" +
                                    "NLR: %{y:.0%}<br>" +
                                    "<extra></extra>",
                                    ))
    # STEP 3
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # STEP 4
    figure = {'data': data,
              'layout': go.Layout(
                  margin=dict(b=40, t=10),  # l, r, b, t
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  hovermode='closest',
                  showlegend=True,
                  height=500,
                  autosize=True,
                  # title={'text': 'Net Loss Ratio', 'font': {'color': 'black'}, 'x': 0.5},
                  yaxis=dict(
                      title='Net Loss Ratio (%)',
                      tickformat=".0%",
                      titlefont=dict(
                          family='Arial',
                          size=15,
                          color='lightgrey')
                  ),
                  xaxis=dict(
                      title='Reporting Year',
                      titlefont=dict(
                          family='Arial',
                          size=15,
                          color='lightgrey')
                  ),
              ),
              }

    return figure


# Graph 3 - Net Loss Ratio - Box Chart
@app.callback(Output('lossratio_box', 'figure'),
              [Input('lobselector', 'value')])
def update_lossratio_box(lobselector):
    # STEP 1
    trace = []
    # STEP 2
    # Draw and append traces for each stock
    for lob in lobselector:
        df_nlr = df2[['year', 'insurer_name', 'Description', lob]]
        df_nlr = df_nlr[df_nlr.Description == 'Net Loss Ratio']
        df_nlr = df_nlr[df_nlr[lob] != 0]  # remove data where there is 0 loss ratio
        trace.append(go.Box(x=df_nlr['year'].tolist(),
                            y=df_nlr[lob].tolist(),
                            quartilemethod="linear",
                            opacity=0.7,
                            name=lob,
                            boxpoints='all',
                            marker_size=3,
                            jitter=0.3,
                            text=df_nlr['insurer_name'] + " - " + lob,
                            hovertemplate=
                            "<b>%{text}</b><br>" +
                            "Year: %{x:.f}<br>" +
                            "NLR: %{y:.0%}<br>" +
                            "<extra></extra>",
                            ))
    # STEP 3
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # STEP 4
    figure = {'data': data,
              'layout': go.Layout(
                  margin=dict(b=40, t=10),  # l, r, b, t
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  hovermode='closest',
                  height=400,
                  showlegend=True,
                  autosize=True,
                  yaxis=dict(
                      range=[-0.3, 2],
                      title='Net Loss Ratio (%)',
                      tickformat=".0%",
                      titlefont=dict(
                          family='Arial',
                          size=15,
                          color='lightgrey')
                  ),
                  xaxis=dict(
                      title='Reporting Year',
                      titlefont=dict(
                          family='Arial',
                          size=15,
                          color='lightgrey')
                  ),
              ),
              }

    return figure


# Graph 4 - Combined Ratio - Box Chart
@app.callback(Output('cor_box', 'figure'),
              [Input('lobselector', 'value')])
def update_cor_box(lobselector):
    # STEP 1
    trace = []
    # STEP 2
    # Draw and append traces for each stock
    for lob in lobselector:
        df_nlr = df2[['year', 'insurer_name', 'Description', lob]]
        df_nlr = df_nlr[df_nlr.Description == 'Combined Operating Ratio']
        df_nlr = df_nlr[df_nlr[lob] != 0]  # remove data where there is 0 loss ratio
        trace.append(go.Box(x=df_nlr['year'].tolist(),
                            y=df_nlr[lob].tolist(),
                            quartilemethod="linear",
                            opacity=0.7,
                            name=lob,
                            boxpoints='all',
                            marker_size=3,
                            jitter=0.3,
                            text=df_nlr['insurer_name'] + " - " + lob,
                            hovertemplate=
                            "<b>%{text}</b><br>" +
                            "Year: %{x:.f}<br>" +
                            "COR: %{y:.0%}<br>" +
                            "<extra></extra>",
                            ))
    # STEP 3
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # STEP 4
    figure = {'data': data,
              'layout': go.Layout(
                  margin=dict(b=40, t=10),  # l, r, b, t
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  hovermode='closest',
                  height=400,
                  showlegend=True,
                  autosize=True,
                  yaxis=dict(
                      range=[0, 2],
                      title='Net to Gross Ratio (%)',
                      tickformat=".0%",
                      titlefont=dict(
                          family='Arial',
                          size=15,
                          color='lightgrey')
                  ),
                  xaxis=dict(
                      title='Reporting Year',
                      titlefont=dict(
                          family='Arial',
                          size=15,
                          color='lightgrey')
                  ),
              ),
              }

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
