import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import statsmodels.formula.api as sm
from scipy.stats import pearsonr
from statsmodels.compat import lzip
import statsmodels.stats.api as sms
import plotly.graph_objects as go
df = pd.read_csv('Data/Master_Data.csv', converters={'countyfips': str})

# Add Code
def fips_code(x):
    if len(x) == 4:
        return "0" + str(x)
    else:
        return str(x)
# Apply function
df['countyfips'] = df['countyfips'].apply(fips_code)

# Unique State and Countys
# States
states = df['statedesc'].unique()
states = sorted(states)
# Countys
countys = df['countyname'].unique()
countys = sorted(countys)

# Import ploty and other dependancies
import plotly.express as px
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(children=[
                html.H1(
                    children="Asthma Societal Impact Dashboard",style={'textAlign': 'center'}, className="header-title" 
                ), #Header title
                html.H3(
                    children="About", className="about-heading"
                ),
                html.Label(
                    children='''Asthma is a lung disease that impacts approximately 26 million Americans. For those that have asthma exposure to pollution and smoke might heighten symptoms, while for others, 
                    exposure can cause asthma to develop for the very first time. Individuals who smoke are also at a higher risk of developing asthma symptoms. Because asthma has no permanent cure our focus will be on 
                    prevention of future asthma rates, with a focus on how reductions today could impact the population (age 19-64) by 2030 based on birth rate data from the United States Census Bureau.'''
                    ,
                    className="header-description",
                ),
                html.H3(
                    children="Analysis Description", className="analysis-heading"
                ),
                html.Label(
                    children='''Utilizing data collected from the Environmental Protection Agency (EPA) and Centers for Disease Control and Prevention (CDC) analysis was conducted, among individuals
                    ages 19 to 64, to examine factors that impact asthma rates and determine how changes in these factors can reduce asthma rates over the course of a ten year period (between 2020 and 2030). 
                    To do this, Census data was obtained to estimate the change in population of individuals age 19 to 64 over this 10 year time period. The obtained regression coefficients, using a Fixed Effects Model, can thus be applied to examine 
                    how changes to various factors may help reduce estimated asthma cases. Additionally, using this methodology a monetary value to reduced asthma cases can be assigned to determine the societal return 
                    (quantified in USD) over this time period.                    
                    '''
                    ,
                    className="analysis-description"
                ),
                html.H3(
                    children="Dashboard Functionality", className="function-heading"
                ),
                html.Label(
                    children='''Results from this analysis can be viewed at the individual county level, for which the Fixed Effects Model was run, or the aggregated impacts (across all Counties) can be viewed by State.
                    The sliders on the right side of the dashboard allow users to examine impacts to the dependent variable (which can be changed in the Metric Selected parameter) when changes are made to these factors, these 
                    factors being:
                    '''
                    ,
                    className="dashboard-description"
                ),
                dcc.Markdown('''
                    * Reduced Particulate Matter 2.5 (PM 2.5) Emissions
                    * Reduced Smoking Rates (Among individuals ages 19 to 64)
                    * Increased health care accessibility (Among individuals ages 19 to 64)                  
                '''),
                html.H3(
                    children="Github Repository", className="github-heading"
                ),
                html.Label(
                    children='''For more information about this analysis please find my Github in the following link: '''
                    ,
                    className="github-description"
                ),
                html.Label(['', html.A('My Github', href='https://github.com/1ceisen/Udacity-Capstone-Project-Asthma-Reduction-Analysis')]),
                
                    
            ],
            className="header",style={'backgroundColor':'#75B3E0'},
        ), #Description below the header
    
    html.Br(),
    html.Div(children=[
        html.H4('State vs. County View'),
        html.Label('View data aggregated at either the State or County level'),
        dcc.RadioItems(id='geo-level',
            options=[
                {'label': 'State', 'value': 'ST'},
                {'label': 'County', 'value': 'CT'}
            ],
            value='CT'
        ),
        
        html.Br(),
        html.H4('Metric Selected'),
        html.Label('Select metric you wish to view'),
        dcc.RadioItems(id='metric-selected',
            options=[
                {'label': 'Total Monetary Value of Reduced Asthma Cases ($100,000 USD)', 'value': 'Total Monetary Value of Reduced Asthma Cases ($100,000 USD)'},
                {'label': 'Total Reduced Asthma Cases', 'value': 'Total Reduced Asthma Cases'},
                {'label': 'Asthma Rates', 'value': 'Asthma Rates'}
            ],
            value='Total Monetary Value of Reduced Asthma Cases ($100,000 USD)',
            labelStyle={'display': 'flex'}
        ),  ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw', 'width': '33%'}),     
        
    html.Div(children=[
        html.H4('State Dropdown'),
        dcc.Dropdown(id="state-filter",
            options=[{'value': State, 'label': State}
                       for State in states], multi=True
        ),

        html.Br(),
        html.H4('County Dropdown'),
        dcc.Dropdown(id="county-filter",
            options=[{'value': x, 'label': x}
                       for x in countys], multi=True
        ),  ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw', 'width': '25%'}),

    html.Div(children=[   
        html.H4('Reduced PM 2.5 Emissions Percentage Impact'),
        dcc.Slider(
            id = "emissions-slider",
            min=0,
            max=5,
            step=0.1,
            marks={i: '{}'.format(i) if i == 1 else str(i) for i in range(0, 6)},
            value=0,
        ), html.Div(id='emissions-output-container'),
        
        html.Br(),
        html.H4('Reduced Smoking Rates Percentage Impact'),
        dcc.Slider(
            id = "smoking-slider",
            min=0,
            max=5,
            step=0.1,
            marks={i: '{}'.format(i) if i == 1 else str(i) for i in range(0, 6)},
            value=0,
        ), html.Div(id='smoking-output-container'),

        html.Br(),
        html.H4('Increased Health Care Accessibility Percentage Impact'),
        dcc.Slider(
            id = "healthcare-slider",
            min=0,
            max=5,
            step=0.1,
            marks={i: '{}'.format(i) if i == 1 else str(i) for i in range(0, 6)},
            value=0,
        ), html.Div(id='healthcare-output-container'),
    ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw', 'width': '30%'}),
    
    html.Br(),
    html.Div(id='metric-selected-container', style = {'padding-top':'5%'}),
    
    html.Div(children=[
        dcc.Graph(id="choropleth")], style={'display': 'block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw'}),
        
    html.Div(children=[
                html.H3(
                    children="Variable Definitions", className="var-heading"
                ),
                html.H4('Total Monetary Value of Reduced Asthma Cases ($100,000 USD)'),
                dcc.Markdown('''
                    * Reduced_Emissions_Monetary_Impact: Estimated monetary value of reduced asthma cases associated with reduced PM25 emissions
                    * Reduced_Smoking_Monetary_Impact: Estimated monetary value of reduced asthma cases associated with reduced smoking rates
                    * Increased_Healthcare_Access_Monetary_Impact: Estimated monetary value of reduced asthma cases associated with increased healthcare accessibility
                    * Total_Monetary_Impact: Estimated monetary impact of reduced asthma cases associated with all factors examined                    
                '''),
                html.H4('Total Reduced Asthma Cases'),
                dcc.Markdown('''
                    * Reduced_Emissions_Impact: Estimated number of reduced asthma cases associated with reduced PM25 emissions
                    * Reduced_Smoking_Impact: Estimated number of reduced asthma cases associated with reduced smoking rates
                    * Increased_Healthcare_Access_Impact: Estimated number of reduced asthma cases associated with increased healthcare accessibility
                    * Total_Impact: Estimated number of reduced asthma cases associated with all factors examined
                '''),
                html.H4('Asthma Rates'),
                dcc.Markdown('''
                    * Asthma Rates: Asthma rates across each County or State
                '''),
            ],
            className="header",style={'backgroundColor':'#F0F8F9'},
        ),
], style={'backgroundColor':'#F0F8F9'})

@app.callback(
    dash.dependencies.Output('emissions-output-container', 'children'),
    [dash.dependencies.Input('emissions-slider', 'value')])
def update_output(value):
    return 'Percentage Impact = "{0:.1f}%"'.format(value)

@app.callback(
    dash.dependencies.Output('smoking-output-container', 'children'),
    [dash.dependencies.Input('smoking-slider', 'value')])
def update_output(value):
    return 'Percentage Impact = "{0:.1f}%"'.format(value)
    
@app.callback(
    dash.dependencies.Output('healthcare-output-container', 'children'),
    [dash.dependencies.Input('healthcare-slider', 'value')])
def update_output(value):
    return 'Percentage Impact = "{0:.1f}%"'.format(value)
    
@app.callback(
    dash.dependencies.Output('metric-selected-container', 'children'),
    [dash.dependencies.Input('metric-selected', 'value')])
def update_output(value):
    return html.H2('{}'.format(value))
    

@app.callback(
    dash.dependencies.Output("choropleth", "figure"),
    [dash.dependencies.Input("geo-level", "value"),
    dash.dependencies.Input("state-filter", "value"),
    dash.dependencies.Input("county-filter", "value"),
    dash.dependencies.Input("metric-selected", "value"),
    dash.dependencies.Input("emissions-slider", "value"),
    dash.dependencies.Input("smoking-slider", "value"),
    dash.dependencies.Input("healthcare-slider", "value")])

def display_choropleth(Geo, State, County, Metric, Emissions, Smoking, Healthcare):


#####################################################################################################################################################################################################################################


    ## Run Model ##
        
    fixed_model = sm.ols(formula='''casthma_adjprev ~ np.log(state_emissions) + csmoking_adjprev +
                    access2_adjprev + np.log(per_capita_income) + C(statedesc)''',
                          data=df).fit()
                          
    ## Obtain coefficients ##
        
    state_emissions_coef = pd.read_html(fixed_model.summary2().as_html())[1][1][51]
    state_emissions_coef = f = float(state_emissions_coef)
    csmoking_adjprev_coef = pd.read_html(fixed_model.summary2().as_html())[1][1][52]
    csmoking_adjprev_coef = f = float(csmoking_adjprev_coef)
    access2_adjprev_coef = pd.read_html(fixed_model.summary2().as_html())[1][1][53]
    access2_adjprev_coef = f = float(access2_adjprev_coef)
        
    ## Emissions Impact ##
        
    # Estimated number of reduced asthma cases by county
    df['Reduced_Emissions_Impact'] = (df['net_growth_19to64'] * (df['casthma_adjprev']/100)) - (df['net_growth_19to64'] * ((df['casthma_adjprev'] - (state_emissions_coef*Emissions))/100))
    # Convert to int
    df['Reduced_Emissions_Impact'] = df['Reduced_Emissions_Impact'].astype(int)
    # Apply monetary societal benefit
    df['Reduced_Emissions_Monetary_Impact'] =  (df['Reduced_Emissions_Impact'] * 3100) / 100000
    # State aggregation - monetary societal benefit
    df['Reduced_Emissions_Monetary_Impact_State'] = (df['Reduced_Emissions_Impact'] * 3100)
        
    ## Smoking Impact ##
        
    # Estimated number of reduced asthma cases by county
    df['Reduced_Smoking_Impact'] = (df['net_growth_19to64'] * (df['casthma_adjprev']/100)) - (df['net_growth_19to64'] * ((df['casthma_adjprev'] - (csmoking_adjprev_coef*Smoking))/100))
    # Convert to int
    df['Reduced_Smoking_Impact'] = df['Reduced_Smoking_Impact'].astype(int)
    # Apply monetary societal benefit
    df['Reduced_Smoking_Monetary_Impact'] = (df['Reduced_Smoking_Impact'] * 3100) / 100000
    # State aggregation - monetary societal benefit
    df['Reduced_Smoking_Monetary_Impact_State'] = (df['Reduced_Smoking_Impact'] * 3100)
        
    ## Healthcare Impact ##
        
    # Estimated number of reduced asthma cases by county
    df['Increased_Healthcare_Access_Impact'] = (df['net_growth_19to64'] * (df['casthma_adjprev']/100)) - (df['net_growth_19to64'] * ((df['casthma_adjprev'] - (-access2_adjprev_coef*Healthcare))/100))
    # Convert to int
    df['Increased_Healthcare_Access_Impact'] = df['Increased_Healthcare_Access_Impact'].astype(int)
    # Apply monetary societal benefit
    df['Increased_Healthcare_Access_Monetary_Impact'] = (df['Increased_Healthcare_Access_Impact'] * 3100) / 100000
    # State aggregation - monetary societal benefit
    df['Increased_Healthcare_Access_Monetary_Impact_State'] = (df['Increased_Healthcare_Access_Impact'] * 3100)
        
    ## Total Impact ##
        
    # Estimated total number of reduced asthma case by county
    df['Total_Impact'] = df['Increased_Healthcare_Access_Impact'] + df['Reduced_Smoking_Impact'] + df['Reduced_Emissions_Impact']
    # Convert to int
    df['Total_Impact'] = df['Total_Impact'].astype(int)
    # Apply monetary societal benefit
    df['Total_Monetary_Impact'] = (df['Total_Impact'] * 3100) / 100000
    # State aggregation - monetary societal benefit
    df['Total_Monetary_Impact_State'] = (df['Total_Impact'] * 3100)
        

#####################################################################################################################################################################################################################################


    ### Scenario 1 (Default) ###
    
    # View = County
    # Metric = Monetary Value
    # State Dropdown = None
    # County Dropdown = None
    
    if Geo == 'CT' and State is None and County is None and Metric == 'Total Monetary Value of Reduced Asthma Cases ($100,000 USD)':       
        
        fig = px.choropleth(
            df, geojson=counties, locations='countyfips', color='Total_Monetary_Impact',
            color_continuous_scale="Viridis",
            range_color=(0, np.max(df['Total_Monetary_Impact'])),
            scope="usa",
            hover_name="countyname",
            hover_data=["statedesc", "Reduced_Emissions_Monetary_Impact", "Reduced_Smoking_Monetary_Impact", "Increased_Healthcare_Access_Monetary_Impact"],
            labels={'Total_Monetary_Impact'})
        fig.update_layout(
            height=500, width = 1300, margin={"r":0,"t":0,"l":0,"b":0})

        return fig
 

#####################################################################################################################################################################################################################################


    ### Scenario 2 ###
    
    # View = County
    # Metric = Total Cases
    # State Dropdown = None
    # County Dropdown = None
    
    if Geo == 'CT' and State is None and County is None and Metric == 'Total Reduced Asthma Cases':       
        
        fig = px.choropleth(
            df, geojson=counties, locations='countyfips', color='Total_Impact',
            color_continuous_scale="Viridis",
            range_color=(0, np.max(df['Total_Impact'])),
            scope="usa",
            hover_name="countyname",
            hover_data=["statedesc", "Reduced_Emissions_Impact", "Reduced_Smoking_Impact", "Increased_Healthcare_Access_Impact"],
            labels={'Total_Impact'})
        fig.update_layout(
            height=500, width = 1300, margin={"r":0,"t":0,"l":0,"b":0})

        return fig


#####################################################################################################################################################################################################################################


    ### Scenario 3 ###
    
    # View = County
    # Metric = Asthma Rates
    # State Dropdown = None
    # County Dropdown = None

    if Geo == 'CT' and State is None and County is None and Metric == 'Asthma Rates':       
        
        fig = px.choropleth(
            df, geojson=counties, locations='countyfips', color='casthma_adjprev',
            color_continuous_scale="Viridis",
            range_color=(7, np.max(df['casthma_adjprev'])),
            scope="usa",
            hover_name="countyname",
            hover_data={"statedesc"},
            labels={'casthma_adjprev':'Asthma Rates'})
        fig.update_layout(
            height=500, width = 1300, margin={"r":0,"t":0,"l":0,"b":0})

        return fig


#####################################################################################################################################################################################################################################


    ### Scenario 4 ###
    
    # View = State
    # Metric = Monetary Value
    # State Dropdown = None
    # County Dropdown = None

    if Geo == 'ST' and State is None and County is None and Metric == 'Total Monetary Value of Reduced Asthma Cases ($100,000 USD)': 

        dff = df.groupby(['stateabbr', 'statedesc']).agg({
        'Reduced_Emissions_Monetary_Impact_State':'sum',
        'Reduced_Smoking_Monetary_Impact_State':'sum',
        'Increased_Healthcare_Access_Monetary_Impact_State':'sum',
        'Total_Monetary_Impact_State':'sum'
        }).reset_index()
        
        # Emissions Impact
        dff = dff.rename(columns={'Reduced_Emissions_Monetary_Impact_State': 'Reduced_Emissions_Monetary_Impact'})
        dff['Reduced_Emissions_Monetary_Impact'] = dff['Reduced_Emissions_Monetary_Impact'].astype(int)
        dff['Reduced_Emissions_Monetary_Impact'] = dff['Reduced_Emissions_Monetary_Impact'] / 100000
        
        # Smoking Impact
        dff = dff.rename(columns={'Reduced_Smoking_Monetary_Impact_State': 'Reduced_Smoking_Monetary_Impact'})
        dff['Reduced_Smoking_Monetary_Impact'] = dff['Reduced_Smoking_Monetary_Impact'].astype(int)
        dff['Reduced_Smoking_Monetary_Impact'] = dff['Reduced_Smoking_Monetary_Impact'] / 100000
        
        # Healthcare Impact
        dff = dff.rename(columns={'Increased_Healthcare_Access_Monetary_Impact_State': 'Increased_Healthcare_Access_Monetary_Impact'})
        dff['Increased_Healthcare_Access_Monetary_Impact'] = dff['Increased_Healthcare_Access_Monetary_Impact'].astype(int)
        dff['Increased_Healthcare_Access_Monetary_Impact'] = dff['Increased_Healthcare_Access_Monetary_Impact'] / 100000
        
        # Total Impact
        dff = dff.rename(columns={'Total_Monetary_Impact_State': 'Total_Monetary_Impact'})
        dff['Total_Monetary_Impact'] = dff['Total_Monetary_Impact'].astype(int)
        dff['Total_Monetary_Impact'] = dff['Total_Monetary_Impact'] / 100000
        
        fig = px.choropleth(
            dff, locations='stateabbr', locationmode="USA-states", color='Total_Monetary_Impact',
            color_continuous_scale="Viridis",
            range_color=(0, np.max(dff['Total_Monetary_Impact'])),
            scope="usa",
            hover_name="statedesc",
            hover_data=["Reduced_Emissions_Monetary_Impact", "Reduced_Smoking_Monetary_Impact", "Increased_Healthcare_Access_Monetary_Impact"],
            labels={'Total_Monetary_Impact'})
        fig.update_layout(
            height=500, width = 1300, margin={"r":0,"t":0,"l":0,"b":0})

        return fig


#####################################################################################################################################################################################################################################


    ### Scenario 5 ###
    
    # View = State
    # Metric = Total Cases
    # State Dropdown = None
    # County Dropdown = None

    if Geo == 'ST' and State is None and County is None and Metric == 'Total Reduced Asthma Cases': 

        dff = df.groupby(['stateabbr', 'statedesc']).agg({
        'Reduced_Emissions_Impact':'sum',
        'Reduced_Smoking_Impact':'sum',
        'Increased_Healthcare_Access_Impact':'sum',
        'Total_Impact':'sum'
        }).reset_index()
        
        fig = px.choropleth(
            dff, locations='stateabbr', locationmode="USA-states", color='Total_Impact',
            color_continuous_scale="Viridis",
            range_color=(0, np.max(dff['Total_Impact'])),
            scope="usa",
            hover_name="statedesc",
            hover_data=["Reduced_Emissions_Impact", "Reduced_Smoking_Impact", "Increased_Healthcare_Access_Impact"],
            labels={'Total_Impact'})
        fig.update_layout(
            height=500, width = 1300, margin={"r":0,"t":0,"l":0,"b":0})

        return fig


#####################################################################################################################################################################################################################################

 
    ### Scenario 6 ###
    
    # View = State
    # Metric = Asthma Rates
    # State Dropdown = None
    # County Dropdown = None 
 
    if Geo == 'ST' and State is None and County is None and Metric == 'Asthma Rates': 

        df['Total_Asthma_Cases'] = df['totalpopulation'] * df['casthma_adjprev']
        
        dff = df.groupby(['stateabbr', 'statedesc']).agg({
        'totalpopulation':'sum',
        'Total_Asthma_Cases':'sum'
        }).reset_index()
        
        dff['Asthma_Rate'] = dff['Total_Asthma_Cases'] / dff['totalpopulation']
        
        fig = px.choropleth(
            dff, locations='stateabbr', locationmode="USA-states", color='Asthma_Rate',
            color_continuous_scale="Viridis",
            range_color=(6, np.max(dff['Asthma_Rate'])),
            scope="usa",
            hover_name="statedesc",
            hover_data=['stateabbr', 'statedesc'],
            labels={'Asthma_Rate':'Asthma Rates'})
        fig.update_layout(
            height=500, width = 1300, margin={"r":0,"t":0,"l":0,"b":0})

        return fig
 
 
#####################################################################################################################################################################################################################################
 

    ### Scenario 7 ###
    
    # View = County
    # Metric = Monetary Value
    # State Dropdown = Not None
    # County Dropdown = None

    if Geo == 'CT' and State is not None and County is None and Metric == 'Total Monetary Value of Reduced Asthma Cases ($100,000 USD)':       

        dff = df.loc[df.statedesc.str.contains('|'.join(State))]
        
        fig = px.choropleth(
            dff, geojson=counties, locations='countyfips', color='Total_Monetary_Impact',
            color_continuous_scale="Viridis",
            range_color=(0, np.max(df['Total_Monetary_Impact'])),
            scope="usa",
            hover_name="countyname",
            hover_data=["statedesc", "Reduced_Emissions_Monetary_Impact", "Reduced_Smoking_Monetary_Impact", "Increased_Healthcare_Access_Monetary_Impact"],
            labels={'Total_Monetary_Impact'})
        fig.update_layout(
            height=500, width = 1300, margin={"r":0,"t":0,"l":0,"b":0})

        return fig  
 
 
#####################################################################################################################################################################################################################################


    ### Scenario 8 ###
    
    # View = County
    # Metric = Monetary Value
    # State Dropdown = Not None
    # County Dropdown = Not None

    if Geo == 'CT' and State is not None and County is not None and Metric == 'Total Monetary Value of Reduced Asthma Cases ($100,000 USD)':       
        
        dff = df.loc[df.statedesc.str.contains('|'.join(State)) & df.countyname.str.contains('|'.join(County))]
        
        fig = px.choropleth(
            dff, geojson=counties, locations='countyfips', color='Total_Monetary_Impact',
            color_continuous_scale="Viridis",
            range_color=(0, np.max(df['Total_Monetary_Impact'])),
            scope="usa",
            hover_name="countyname",
            hover_data=["statedesc", "Reduced_Emissions_Monetary_Impact", "Reduced_Smoking_Monetary_Impact", "Increased_Healthcare_Access_Monetary_Impact"],
            labels={'Total_Monetary_Impact'})
        fig.update_layout(
            height=500, width = 1300, margin={"r":0,"t":0,"l":0,"b":0})

        return fig 
        
        
#####################################################################################################################################################################################################################################


    ### Scenario 9 ###
    
    # View = County
    # Metric = Monetary Value
    # State Dropdown = None
    # County Dropdown = Not None
 
    if Geo == 'CT' and County is not None and Metric == 'Total Monetary Value of Reduced Asthma Cases ($100,000 USD)':       
        
        dff = df.loc[df.countyname.str.contains('|'.join(County))]
        
        fig = px.choropleth(
            dff, geojson=counties, locations='countyfips', color='Total_Monetary_Impact',
            color_continuous_scale="Viridis",
            range_color=(0, np.max(df['Total_Monetary_Impact'])),
            scope="usa",
            hover_name="countyname",
            hover_data=["statedesc", "Reduced_Emissions_Monetary_Impact", "Reduced_Smoking_Monetary_Impact", "Increased_Healthcare_Access_Monetary_Impact"],
            labels={'Total_Monetary_Impact'})
        fig.update_layout(
            height=500, width = 1300, margin={"r":0,"t":0,"l":0,"b":0})

        return fig           


#####################################################################################################################################################################################################################################


    ### Scenario 10 ###
    
    # View = County
    # Metric = Total Cases
    # State Dropdown = Not None
    # County Dropdown = Not None

    if Geo == 'CT' and State is not None and County is None and Metric == 'Total Reduced Asthma Cases':       
        
        dff = df.loc[df.statedesc.str.contains('|'.join(State))]
        
        fig = px.choropleth(
            dff, geojson=counties, locations='countyfips', color='Total_Impact',
            color_continuous_scale="Viridis",
            range_color=(0, np.max(df['Total_Impact'])),
            scope="usa",
            hover_name="countyname",
            hover_data=["statedesc", "Reduced_Emissions_Impact", "Reduced_Smoking_Impact", "Increased_Healthcare_Access_Impact"],
            labels={'Total_Impact'})
        fig.update_layout(
            height=500, width = 1300, margin={"r":0,"t":0,"l":0,"b":0})

        return fig 
        

#####################################################################################################################################################################################################################################


    ### Scenario 11 ###
    
    # View = County
    # Metric = Total Cases
    # State Dropdown = Not None
    # County Dropdown = Not None

    if Geo == 'CT' and State is not None and County is not None and Metric == 'Total Reduced Asthma Cases':       
        
        dff = df.loc[df.statedesc.str.contains('|'.join(State)) & df.countyname.str.contains('|'.join(County))]
        
        fig = px.choropleth(
            dff, geojson=counties, locations='countyfips', color='Total_Impact',
            color_continuous_scale="Viridis",
            range_color=(0, np.max(df['Total_Impact'])),
            scope="usa",
            hover_name="countyname",
            hover_data=["statedesc", "Reduced_Emissions_Impact", "Reduced_Smoking_Impact", "Increased_Healthcare_Access_Impact"],
            labels={'Total_Impact'})
        fig.update_layout(
            height=500, width = 1300, margin={"r":0,"t":0,"l":0,"b":0})

        return fig 
 

#####################################################################################################################################################################################################################################


    ### Scenario 12 ###
    
    # View = County
    # Metric = Total Cases
    # State Dropdown = None
    # County Dropdown = Not None

    if Geo == 'CT' and County is not None and Metric == 'Total Reduced Asthma Cases':       
        
        dff = df.loc[df.countyname.str.contains('|'.join(County))]
        
        fig = px.choropleth(
            dff, geojson=counties, locations='countyfips', color='Total_Impact',
            color_continuous_scale="Viridis",
            range_color=(0, np.max(df['Total_Impact'])),
            scope="usa",
            hover_name="countyname",
            hover_data=["statedesc", "Reduced_Emissions_Impact", "Reduced_Smoking_Impact", "Increased_Healthcare_Access_Impact"],
            labels={'Total_Impact'})
        fig.update_layout(
            height=500, width = 1300, margin={"r":0,"t":0,"l":0,"b":0})

        return fig 

 

#####################################################################################################################################################################################################################################


    ### Scenario 13 ###
    
    # View = County
    # Metric = Asthma Rates
    # State Dropdown = Not None
    # County Dropdown = None

    if Geo == 'CT' and State is not None and County is None and Metric == 'Asthma Rates':         
        
        dff = df.loc[df.statedesc.str.contains('|'.join(State))]
        
        fig = px.choropleth(
            dff, geojson=counties, locations='countyfips', color='casthma_adjprev',
            color_continuous_scale="Viridis",
            range_color=(7, np.max(df['casthma_adjprev'])),
            scope="usa",
            hover_name="countyname",
            hover_data={"statedesc"},
            labels={'casthma_adjprev':'Asthma Rates'})
        fig.update_layout(
            height=500, width = 1300, margin={"r":0,"t":0,"l":0,"b":0})

        return fig
        
        
#####################################################################################################################################################################################################################################


    ### Scenario 14 ###
    
    # View = County
    # Metric = Asthma Rates
    # State Dropdown = Not None
    # County Dropdown = None

    if Geo == 'CT' and State is not None and County is not None and Metric == 'Asthma Rates':       
        
        dff = df.loc[df.statedesc.str.contains('|'.join(State)) & df.countyname.str.contains('|'.join(County))]
        
        fig = px.choropleth(
            dff, geojson=counties, locations='countyfips', color='casthma_adjprev',
            color_continuous_scale="Viridis",
            range_color=(7, np.max(df['casthma_adjprev'])),
            scope="usa",
            hover_name="countyname",
            hover_data={"statedesc"},
            labels={'casthma_adjprev':'Asthma Rates'})
        fig.update_layout(
            height=500, width = 1300, margin={"r":0,"t":0,"l":0,"b":0})

        return fig 


#####################################################################################################################################################################################################################################


    ### Scenario 15 ###
    
    # View = County
    # Metric = Asthma Rates
    # State Dropdown = None
    # County Dropdown = Not None

    if Geo == 'CT' and County is not None and Metric == 'Asthma Rates':       
        
        dff = df.loc[df.countyname.str.contains('|'.join(County))]
        
        fig = px.choropleth(
            dff, geojson=counties, locations='countyfips', color='casthma_adjprev',
            color_continuous_scale="Viridis",
            range_color=(7, np.max(df['casthma_adjprev'])),
            scope="usa",
            hover_name="countyname",
            hover_data={"statedesc"},
            labels={'casthma_adjprev':'Asthma Rates'})
        fig.update_layout(
            height=500, width = 1300, margin={"r":0,"t":0,"l":0,"b":0})

        return fig 


#####################################################################################################################################################################################################################################


    ### Scenario 16 ###
    
    # View = State
    # Metric = Monetary Value
    # State Dropdown = Not None
    # County Dropdown = None

    if Geo == 'ST' and State is not None and Metric == 'Total Monetary Value of Reduced Asthma Cases ($100,000 USD)':       

        dff = df.loc[df.statedesc.str.contains('|'.join(State))]

        dfff = dff.groupby(['stateabbr', 'statedesc']).agg({
        'Reduced_Emissions_Monetary_Impact_State':'sum',
        'Reduced_Smoking_Monetary_Impact_State':'sum',
        'Increased_Healthcare_Access_Monetary_Impact_State':'sum',
        'Total_Monetary_Impact_State':'sum'
        }).reset_index()
        
        # Emissions Impact
        dfff = dfff.rename(columns={'Reduced_Emissions_Monetary_Impact_State': 'Reduced_Emissions_Monetary_Impact'})
        dfff['Reduced_Emissions_Monetary_Impact'] = dfff['Reduced_Emissions_Monetary_Impact'].astype(int)
        dfff['Reduced_Emissions_Monetary_Impact'] = dfff['Reduced_Emissions_Monetary_Impact'] / 100000
        
        # Smoking Impact
        dfff = dfff.rename(columns={'Reduced_Smoking_Monetary_Impact_State': 'Reduced_Smoking_Monetary_Impact'})
        dfff['Reduced_Smoking_Monetary_Impact'] = dfff['Reduced_Smoking_Monetary_Impact'].astype(int)
        dfff['Reduced_Smoking_Monetary_Impact'] = dfff['Reduced_Smoking_Monetary_Impact'] / 100000
        
        # Healthcare Impact
        dfff = dfff.rename(columns={'Increased_Healthcare_Access_Monetary_Impact_State': 'Increased_Healthcare_Access_Monetary_Impact'})
        dfff['Increased_Healthcare_Access_Monetary_Impact'] = dfff['Increased_Healthcare_Access_Monetary_Impact'].astype(int)
        dfff['Increased_Healthcare_Access_Monetary_Impact'] = dfff['Increased_Healthcare_Access_Monetary_Impact'] / 100000
        
        # Total Impact
        dfff = dfff.rename(columns={'Total_Monetary_Impact_State': 'Total_Monetary_Impact'})
        dfff['Total_Monetary_Impact'] = dfff['Total_Monetary_Impact'].astype(int)
        dfff['Total_Monetary_Impact'] = dfff['Total_Monetary_Impact'] / 100000
        
        fig = px.choropleth(
            dfff, locations='stateabbr', locationmode="USA-states", color='Total_Monetary_Impact',
            color_continuous_scale="Viridis",
            range_color=(0, np.max(dff['Total_Monetary_Impact'])),
            scope="usa",
            hover_name="statedesc",
            hover_data=["Reduced_Emissions_Monetary_Impact", "Reduced_Smoking_Monetary_Impact", "Increased_Healthcare_Access_Monetary_Impact"],
            labels={'Total_Monetary_Impact'})
        fig.update_layout(
            height=500, width = 1300, margin={"r":0,"t":0,"l":0,"b":0})

        return fig


#####################################################################################################################################################################################################################################


    ### Scenario 17 ###
    
    # View = State
    # Metric = Total Cases
    # State Dropdown = Not None
    # County Dropdown = None

    if Geo == 'ST' and State is not None and Metric == 'Total Reduced Asthma Cases':       

        dff = df.loc[df.statedesc.str.contains('|'.join(State))]

        dfff = dff.groupby(['stateabbr', 'statedesc']).agg({
        'Reduced_Emissions_Impact':'sum',
        'Reduced_Smoking_Impact':'sum',
        'Increased_Healthcare_Access_Impact':'sum',
        'Total_Impact':'sum'
        }).reset_index()
        
        fig = px.choropleth(
            dfff, locations='stateabbr', locationmode="USA-states", color='Total_Impact',
            color_continuous_scale="Viridis",
            range_color=(0, np.max(dff['Total_Impact'])),
            scope="usa",
            hover_name="statedesc",
            hover_data=["Reduced_Emissions_Impact", "Reduced_Smoking_Impact", "Increased_Healthcare_Access_Impact"],
            labels={'Total_Impact'})
        fig.update_layout(
            height=500, width = 1300, margin={"r":0,"t":0,"l":0,"b":0})

        return fig


#####################################################################################################################################################################################################################################


    ### Scenario 18 ###
    
    # View = State
    # Metric = Asthma Rates
    # State Dropdown = Not None
    # County Dropdown = None

    if Geo == 'ST' and State is not None and Metric == 'Asthma Rates':       

        dff = df.loc[df.statedesc.str.contains('|'.join(State))] 

        dff['Total_Asthma_Cases'] = dff['totalpopulation'] * dff['casthma_adjprev']
        
        dfff = dff.groupby(['stateabbr', 'statedesc']).agg({
        'totalpopulation':'sum',
        'Total_Asthma_Cases':'sum'
        }).reset_index()
        
        dfff['Asthma_Rate'] = dfff['Total_Asthma_Cases'] / dfff['totalpopulation']
        
        fig = px.choropleth(
            dfff, locations='stateabbr', locationmode="USA-states", color='Asthma_Rate',
            color_continuous_scale="Viridis",
            range_color=(6, np.max(dfff['Asthma_Rate'])),
            scope="usa",
            hover_name='statedesc',
            labels={'Asthma_Rate':'Asthma Rates'})
        fig.update_layout(
            height=500, width = 1300, margin={"r":0,"t":0,"l":0,"b":0})

        return fig


if __name__ == '__main__':
    app.run_server(debug=True)