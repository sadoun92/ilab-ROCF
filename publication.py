!pip install dimcli plotly networkx pyvis jsonpickle  -U --quiet
import dimcli
from dimcli.shortcuts import *
from dimcli.core.extras import NetworkViz # custom version of pyvis - colab-compatible

import sys, time, json
from tqdm.notebook import tqdm as progressbar
import pandas as pd
import matplotlib.pyplot as plt 
import descartes
import networkx as nx
import plotly.express as px
import itertools

from tqdm.notebook import tqdm as pbar
if not 'google.colab' in sys.modules:
  # make js dependecies local / needed by html exports
  from plotly.offline import init_notebook_mode
  init_notebook_mode(connected=True)


  import getpass
  USERNAME = getpass.getpass(prompt='mohammadkhalil.m.saadoonAPI@student.uts.edu.au' )
  PASSWORD = getpass.getpass(prompt='qpzR38TV')
  dimcli.login(username ="mohammadkhalil.m.saadoonAPI@student.uts.edu.au" , password = "qpzR38TV" )
else:
  dimcli.login(username ="mohammadkhalil.m.saadoonAPI@student.uts.edu.au" , password = "qpzR38TV" )
dsl = dimcli.Dsl()


#------------------------------------------------------------

KEYWORD = "10.1080/20013078.2018.1535750"

q = f"""search publications 
          where research_orgs="grid.117476.2"
            for "\\"{KEYWORD}\\"" 
        return publications[id+title+times_cited+altmetric+concepts_scores] 
        """



data = dsl.query(q)
#concepts = data.as_dataframe_concepts()
#print("Total concepts:", len(concepts))
#print("Concepts score average", concepts['score_avg'].mean())
concepts.head()


#--------------------------------------------------------

KEYWORD = "10.1080/20013078.2018.1535750"

q = f"""search publications 
          where research_orgs="grid.117476.2"
            for "\\"{KEYWORD}\\"" 
        return publications[id+title+times_cited+altmetric+concepts_scores] 
        """



data = dsl.query(q)
#concepts = data.as_dataframe_concepts()
#print("Total concepts:", len(concepts))
#print("Concepts score average", concepts['score_avg'].mean())
concepts.head()

-----------------------------------
res1 = dsl.query("""
 search publications
 where research_orgs="grid.117476.2"
 return publications""", verbose=False)
print(res1.stats)
print("Results in this batch:", res1.count_batch)
print("Results in this total:", res1.count_total)
print("Errors",res1.errors)

#--------------------------------------------

res2 = dsl.query("""
  search grants 
  where research_orgs="grid.117476.2"
  return grants """, verbose=False)
print(res2.stats)
print("Results in this batch:", res2.count_batch)
print("Results in this total:", res2.count_total)
print("Errors",res2.errors)


#----------------------------------------------

%%dsldf 
search publications
where research_orgs="grid.117476.2"
for "Simon Buckingham Shum"
return publications[id+title+year+doi]
#-------------------------------------
%%dsldf 

search publications 
where research_orgs="grid.117476.2"
for "Simon Buckingham Shum"
return publications[id+times_cited+altmetric]

#-------------------------------------------

%%dsldf 
search publications where research_orgs="grid.117476.2" in title_abstract_only for "learning analytics"
return publications
#------------------------------
%%dsldf 
search publications 
in authors for "\"Simon Buckingham Shum\""
return publications

#--------------------------

#research Organization 

tot = dsl.query(f"""search publications where research_orgs.id="{GRIDID}" return publications """, verbose=False).count_total
print(f"{GRIDID} has a total of {tot} publications in Dimensions")
#-----------------------------------

#research Organization 

df = dsl.query(f"""search publications where research_orgs.id="{GRIDID}" return year limit 100""").as_dataframe() 
df.rename(columns={"id": "year"}, inplace=True)
#
px.bar(df, x="year", y="count", 
       title=f"Publications for UTS  {GRIDID} - by year")
     
     
#--------------------------------------------------
# most Publications cited in last 2 years
data = dslquery(f"""search publications where research_orgs.id="{GRIDID}" 
        return publications[doi+title+recent_citations+category_for+journal] 
        sort by recent_citations limit 100""")
df = data.as_dataframe()
df.head(10)[['title', 'doi', 'recent_citations', 'journal.title']]

#-----------------------------------------------
#Most cited publications in UTS in last 2 year
px.bar(df, x="title", y="recent_citations", 
       title=f"Most cited publications in UTS in last 2 year")
       
#--------------------------------------------------


#most Publications cited all time 
data = dslquery(f"""search publications 
                where research_orgs.id="{GRIDID}" 
                return publications[doi+title+times_cited+category_for+journal] 
                sort by times_cited limit 1000""")
df = data.as_dataframe()
df.head(10)[['title', 'doi', 'times_cited', 'journal.title']]

#-----------------------------------------------------
#Most cited publications in UTS
px.bar(df, x="title", y="times_cited", 
       title=f"Most cited publications in UTS   - all time")
       
#----------------------------------------------------------
#Publications most cited : which research areas
data = dslquery(f"""search publications 
                    where research_orgs.id="{GRIDID}" 
                    return publications[doi+title+times_cited+category_for+journal] 
                    sort by times_cited limit 100""")
                    
normalize_key("category_for", data.publications, [])
df = pd.json_normalize(data.publications, record_path='category_for', meta=['doi', 'title', 'times_cited', ], errors='ignore' )
df.head()
px.scatter(df, 
       x="name", y="times_cited", 
       color="name",
       title="Most publication cited & in which research area ")
       
#Most cited publication and in which journals 

data = dslquery(f"""search publications 
                    where research_orgs.id="{GRIDID}" 
                    return publications[doi+title+times_cited+category_for+journal] 
                    sort by times_cited limit 1000""")
            
df = data.as_dataframe()


#Publications from UTS - Journals VS Citations
px.scatter(df, 
           x="times_cited", y="journal.title", 
           marginal_x="histogram", 
           marginal_y="histogram", 
           height=600,
           title="Publications from UTS - Journals VS Citations")
           
           
#Top Funders in UTS by aggregated funding amount 

fundersdata = dsl.query(f"""search grants 
                        where research_orgs.id="{GRIDID}" 
                        return funders aggregate funding 
                        sort by funding""")
df = fundersdata.as_dataframe()
df.head(10)
#Top funders split by country of the funder
px.bar(df, 
       x="name", y="funding", 
       color="country_name",
       title="Funding for UTS")
       
#--------------------------------
#Funding for UTS Publications VS Aggregated Funding Amount
px.scatter(df, 
           x="funding", y="count", 
           color="name", 
           height=600,
           title="Funding for UTS Publications VS Aggregated Funding Amount")


       


