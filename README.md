# Installations
This project requires Python 3.8.5 and the following packages installed

* pandas

* numpy

* scipy

* matplotlib

* dash

* plotly

* statsmodels

* math

* sqldf

# Business Understanding
Asthma is a major respiratory disease that impacts approximately 26 million Amercians. For those that have asthma exposure to pollutants and smoke might heighten symptoms, 
while for others, exposure can cause asthma to develop for the very first time. Individuals who smoke are also at a higher risk of developing asthma symptoms. 
Because asthma has no permanent cure our focus will be on prevention of future asthma rates, with a focus on how reductions today could impact the population (age 19-64) 
by 2030 based on birth rate data from the United States Census Bureau. The estimated cost of asthma is approximately $3,100 USD per person, therefore asthma reduction 
would result in significant societal benefits.  

# Data

Data for this analysis were collected from many different sources, notably the Environmental Protection Agency (EPA) and Centers for Disease Control and Prevention (CDC).
API's were utilized to extract data from these sources in which API calls through the following Jupyter notebooks were used to retieve the raw data required:

* CDC_Data.ipynb: Jupyter notebook connecting to the CDC API to obtain asthma rates, smoking rates and accessibility to healthcare rates at the County level for individuals
ages 19 to 64.

* Capstone - Emissions Data.ipynb: Jupyter notebook connecting to the EPA API to obtain Particulate Matter 2.5 (PM 2.5) emissions at the County level.

* Income.csv: Per-capita household income as the County level. Obtained from the United States Census Bureau

* Parameters: CSV file containing a list of pollutant codes for EPA API call.

# Prepare Data

In order to develop an initiated model for production of the web app, a series of steps to clean the data were needed. All processes, including exploratory analysis, to 
develop the finalized dataframe and model utilized in the web application are included in the Data Model and Regression.ipynb file.

# Data Modeling

Ordinary Least Squares was intitially conducted on the finalized dataframe. After conducting a Breusch-Pagan test, in testing for random effects, we rejected the null hypothesis
of no random effects and thus concluded random effects were present. Because of this a Fixed Effects Model, using State dummy variables as additional controls,
were employed for analysis.

# Evaluation of Results

Regression coefficients for smoking and healthcare accessibility were found statistically significant. County level per-capita household income and emissions were not
statistically significant. Because emissions were a significant control variable from a policy standpoint, an additional Fixed Effects model utilizing average State emissions
was employed. This regression coefficient was found to be significant and this utilized in the web application. Because State governments might have more authority to 
impliment measures to reduce overall PM25 emission rates, this might be a more effective manner to relay the results and enact potential State legislation to reduce
particulate matter levels.

# How to Interact with this project

The web application to view and interact with the outcomes from this analysis are hosted through a Dash application. This application allows users to examine impacts 
to the dependent variable (which can be changed in the Metric Selected parameter) when changes are made to key explanatory variables utilized in the Fixed Effect model (holding
 all other variables constant). Additionally, the results can be examined at the individual County level or aggregated at the State level through a parameter on the dashboard.
 Lastly, State and County filters allow users to key in on specific geographical locations.

## File Description

### data
**Master_Data.csv**: Finalized dataset

### apps
**App.py**: Python script to load web application


## Instructions

**1.** Run the following command in the app's directory to run your web app
 
 >python App.py

 **2.** Go to http://127.0.0.1:8050/ to view Dash app

# Project Writeup

Please check out my blog post for a complete project writeup, including a description in the series of steps to develop this tool.
https://medium.com/@ceisen/impact-of-various-factors-on-asthma-rates-in-the-united-states-7481f333e16b

# Licensing, Authors, Acknowledgements
Credit must be given to the EPA, CDC and United States Census Bureau for the data. Additional credit must go to Udacity for providing a high level template to construct this project while also providing the necessary teachings. 
