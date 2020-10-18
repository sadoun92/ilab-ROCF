!pip install dimcli tqdm -U --quiet 
import csv
import dimcli
from dimcli.shortcuts import *
import sys, time, json
import pandas as pd
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt
%matplotlib inline
from tqdm.notebook import tqdm as progressbar

import plotly.express as px
if not 'google.colab' in sys.modules:
  # make js dependecies local / needed by html exports
  from plotly.offline import init_notebook_mode
  init_notebook_mode(connected=True)


print("==\nLogging in..")
ENDPOINT = "https://app.dimensions.ai"
if 'google.colab' in sys.modules:
  import getpass
  USERNAME = getpass.getpass(prompt='mohammadkhalil.m.saadoonAPI@student.uts.edu.au' )
  PASSWORD = getpass.getpass(prompt='')
  dimcli.login(username ="mohammadkhalil.m.saadoonAPI@student.uts.edu.au" , password = "" )
else:
  dimcli.login(username ="mohammadkhalil.m.saadoonAPI@student.uts.edu.au" , password = "" )
dsl = dimcli.Dsl()


pwd()

#read grant data 

grant_data= pd.read_csv(r"C:\Users\Dell 990\Dimensions-Grant-2020-10-07_00-50-26.csv")
grant_data.head()

grant_data['Start Year']

missing_value=["N/a", "na","N/A,",np.nan]
grant_data= pd.read_csv(r"C:\Users\Dell 990\Dimensions-Grant-2020-10-07_00-50-26.csv",na_values=missing_value)
grant_data.info()

grant_data.info()


#drop rows without a Grant ID 
grant_data.dropna(subset=["Grant ID"], inplace=True)
grant_uts_ids = grant_data['Grant ID'].to_list()

grant_data['Start Year']

grant_data.head(5)

#Extracting linked publications 
#KEYWORD="grid.117476.2"
# the main query

q = """search publications 
             where supporting_grant_ids in {} 
       return publications[title+doi+year+supporting_grant_ids]
       """


# let's loop through all grants IDs in chunks and query Dimensions 

results = []
for chunk in progressbar(list(chunks_of(list(grant_uts_ids), 300))):
    data = dsl.query_iterative(q.format(json.dumps(chunk)), verbose=False)
    results += data.publications
    time.sleep(1)


# put the data into a dataframe, remove duplicates and save

pubs = pd.DataFrame().from_dict(results)
print("Publications found: ", len(pubs))
pubs.drop_duplicates(subset='doi', inplace=True)
print("Unique publications found: ", len(pubs))

pubs['supporting_grant_ids'] = pubs['supporting_grant_ids'].apply(lambda x: ','.join(map(str, x)))

pubs.head(5)

def pubs_for_grantid(grantid):
  global pubs
  return pubs[pubs['supporting_grant_ids'].str.contains(grantid)]
  
  
  l = []
for x in progressbar(grant_uts_ids):
  l.append(len(pubs_for_grantid(x)))
grant_data['Resulting Publications'] = l

grant_data.to_csv("Dimensions-Grant-part2.csv", index=False)
grant_data.head(5)

#grant_data['End Year']= pd.to_numeric(grant_data['End Year'])
#grant_data['Start Year']= pd.to_numeric(grant_data['Start Year'])
#assert grant_data['End Year'].dtype== 'int[ns]'
#assert grant_data['Start Year'].dtype== 'int[ns]'

#grant_data['Start Date']= pd.to_numeric(grant_data['Start Date'])
#rant_data['End Date']= pd.to_numeric(grant_data['End Date'])
#assert grant_data['Start Date'].dtype== 'int[ns]'
#assert grant_data['End Date'].dtype== 'int[ns]'


grant_data.info()


grant_data.isnull().sum()

grant_data.isnull().any()

grant_data.shape

grant_data.describe()

grant_data.values

#sorting 
grant_data.sort_values(["Rank"])

df_grant=grant_data[['Rank','Grant ID','Grant Number','Title','Abstract','Funding Amount in AUD','Start Year','End Year','Researchers','Research Organization - original','Research Organization - standardized','GRID ID','Funder','Funder Country','FOR (ANZSRC) Categories','Resulting Publications']]
df_grant.head(5)

df_grant.info()

#df_grant = df_grant[(grant_data["Research Organization - original"]=="University of Technology Sydney") | (grant_data["Research Organization - standardized"]=="University of Technology Sydney")]
df_grant.sort_values(["Rank"])
print(df_grant)

duplicates = df_grant.duplicated()
print(duplicates)

df_grant.isnull().sum()

sns.heatmap(df_grant.isnull(),yticklabels=False , annot=True, fmt="d" ,linewidths=.5)

df_grant = df_grant.fillna(0)
df_grant

(df_grant[['Start Year','End Year']].astype(int))

df_grant.dropna(how="all")

# Matching grant data with Dimaction API 

%dslloop search grants where research_orgs= "grid.117476.2" return grants



#check about the grant number 
grants_without_number = df_grant[df_grant['Grant Number'].isnull()]
grants_without_number.head(5)

Data Exploration 
#publication per grant by year and funding amount 

px.bar(df_grant,x='End Year', y="Resulting Publications", 
       color="Funding Amount in AUD", 
       hover_name="Title", 
       hover_data=['Grant ID', 'Start Year', 'End Year', 'Funder', 'Funder Country', "Grant Number"],
       title="Publications per grant")
       
       
       #Publications per grant by country

px.bar(df_grant, 
       x="Funder Country", y="Resulting Publications", 
       color="Funder Country", 
       hover_name="Title", 
       hover_data=['Grant ID', 'Start Year', 'End Year', 'Funder', 'Funder Country'],
       title=f"Publications per grant")
       
#Correlation of num of publications to grant length
px.scatter(df_grant.query('`Resulting Publications` > 0'),  
           y="End Year", x="Start Year", 
           size="Resulting Publications",
           color="Funder Country", 
           marginal_x="histogram",
           hover_name="Title", 
           hover_data=['Grant ID', 'Start Year', 'End Year', 'Funder', 'Funder Country'],
           trendline="ols", 
           title=f"Tot Publications vs grant length")
           
           
#Publications by grant funder
funders = df_grant.query('`Resulting Publications` > 0')\
    .groupby(['Funder', 'Funder Country'], as_index=False)\
    .sum().sort_values(by=["Resulting Publications"], ascending=False)
    
    
px.bar(funders,  
       y="Resulting Publications", x="Funder", 
       color="Funder Country",
       hover_name="Funder", 
       hover_data=['Funder', 'Funder Country'], 
       height=500,
       title=f"Funders")
       
#Publications by grant funder vs funding amount
px.scatter(funders,  
           y="Resulting Publications", x="Funding Amount in AUD", 
           color="Funder Country",
           hover_name="Funder", 
           hover_data=['Funder', 'Funder Country'], 
           title=f"Funders")
           
