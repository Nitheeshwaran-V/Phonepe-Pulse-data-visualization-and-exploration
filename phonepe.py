import os
import pandas as pd
import json
import pymysql
import streamlit as st
import plotly.express as px
import requests
import json


# CONNECTION TO MYSQL

connection = pymysql.connect(host = "127.0.0.1", 
                            user = "root", 
                            passwd = "Nitheesh@24", 
                            database = "phonepe"
                            )

cursor = connection.cursor()

# AGGREGATE TRANSACTION DATA FRAME

ATDF = "select * from agg_transaction"
cursor.execute(ATDF)
connection.commit()
atdf = cursor.fetchall()

agg_tran = pd.DataFrame(atdf, columns = ["State", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"])
# agg_tran

# AGGREGATE USER DATA FRAME

AUDF = "select * from agg_user"
cursor.execute(AUDF)
connection.commit()
audf = cursor.fetchall()

agg_user = pd.DataFrame(audf, columns = ["State", "Years", "Quarter", "Brands", "Transaction_count", "Percentages"])
# agg_user

# MAP TRANSACTION DATA FRAME

MTDF = "select * from map_transaction"
cursor.execute(MTDF)
connection.commit()
mtdf = cursor.fetchall()

map_tran = pd.DataFrame(mtdf, columns = ["State", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"])
# map_tran

# MAP USER DATA FRAME

MUDF = "select * from map_user"
cursor.execute(MUDF)
connection.commit()
mudf = cursor.fetchall()

map_user = pd.DataFrame(mudf, columns = ["State", "Years", "Quarter", "Districts", "Registered_users", "App_opens"])
# map_user

# TOP TRANSACTION DATA FRAME

TTDF = "select * from top_transaction"
cursor.execute(TTDF)
connection.commit()
ttdf = cursor.fetchall()

top_tran = pd.DataFrame(ttdf, columns = ["State", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"])
# top_tran

# TOP USER DATA FRAME

TUDF = "select * from top_user"
cursor.execute(TUDF)
connection.commit()
tudf = cursor.fetchall()

top_user = pd.DataFrame(tudf, columns = ["State", "Years", "Quarter", "Pincodes", "Registered_users"])
# top_user

# AGGREGATE TRANSACTION 

def agg_tran_year_count(dfv, years): # COUNT BAR CHART OVERALL
    AT = dfv[dfv["Years"] == years ]
    AT.reset_index(drop = True, inplace = True)

    ATG = AT.groupby("State")[["Transaction_count", "Transaction_amount"]].sum()
    ATG.reset_index(inplace = True)

    fig_A = px.bar(ATG, x = "State", y = "Transaction_count", color = "State", title = f"TRANSACTION COUNT YEAR {years}", height = 750, width = 1000)
    st.plotly_chart(fig_A)

def agg_tran_year_amount(dfv, years):
    AT = dfv[dfv["Years"] == years ]
    AT.reset_index(drop = True, inplace = True)

    ATG = AT.groupby("State")[["Transaction_count", "Transaction_amount"]].sum()
    ATG.reset_index(inplace = True)

    fig_B = px.bar(ATG, x = "State", y = "Transaction_amount", color = "State", title = f"TRANSACTION AMOUNT YEAR {years}", height = 750, width = 1000)
    st.plotly_chart(fig_B)


def choropleth_map_count(dfv, years): # COUNT CHOROPLETH MAP OVERALL
    AT = dfv[dfv["Years"] == years ]
    AT.reset_index(drop = True, inplace = True)

    ATG = AT.groupby("State")[["Transaction_count", "Transaction_amount"]].sum()
    ATG.reset_index(inplace = True)
    
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)

  
    D1 = json.loads(response.content)
    ST_NAMES = []
    for i in D1["features"]:
        ST_NAMES.append(i["properties"]["ST_NM"])

    ST_NAMES.sort()

    fig_I = px.choropleth(ATG, geojson = D1, locations = "State", featureidkey = "properties.ST_NM", 
                          color = "Transaction_count", color_continuous_scale = "Rainbow", 
                          range_color = (ATG["Transaction_count"].min(), ATG["Transaction_count"].max()),
                          title = f"TRANSACTION COUNT OF YEAR {years}", fitbounds = "locations",
                          height = 600, width = 1000)
    fig_I.update_geos(visible = False)
    st.plotly_chart(fig_I)



def choropleth_map_amount(dfv, years): # AMOUNT CHOROPLETH MAP OVERALL
    AT = dfv[dfv["Years"] == years ]
    AT.reset_index(drop = True, inplace = True)

    ATG = AT.groupby("State")[["Transaction_count", "Transaction_amount"]].sum()
    ATG.reset_index(inplace = True)
    
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)

  
    D1 = json.loads(response.content)
    ST_NAMES = []
    for i in D1["features"]:
        ST_NAMES.append(i["properties"]["ST_NM"])

    ST_NAMES.sort()

    fig_I1 = px.choropleth(ATG, geojson = D1, locations = "State", featureidkey = "properties.ST_NM", 
                          color = "Transaction_amount", color_continuous_scale = "Rainbow", 
                          range_color = (ATG["Transaction_amount"].min(), ATG["Transaction_amount"].max()),
                          title = f"TRANSACTION AMOUNT OF YEAR {years}", fitbounds = "locations",
                          height = 600, width = 1000)
    fig_I1.update_geos(visible = False)
    st.plotly_chart(fig_I1)

# AGGREGATE QUARTERLY TRANSACTION STATE WISE
    
def agg_tran_quater_count(dfv, state, years): # COUNT PIE CHART QUARTERLY 
    AT1 = dfv[dfv["Years"] == years]
    AT1.reset_index(drop = True, inplace = True)

    AT1G = AT1[AT1["State"] == state]
    AT1G.reset_index(drop = "index", inplace = True)

    AT1GG = AT1G.groupby("Quarter")[["Transaction_count", "Transaction_amount"]].sum()
    AT1GG.reset_index(inplace = True)

    A = state
    B = A.upper()
    
    fig = px.pie(AT1GG, names = "Quarter", values = "Transaction_count", color = "Quarter", hole = 0.4,
                 title = f"{B}'S {years} QUARTER WISE ANALYSIS", width = 470, height = 470)
    st.plotly_chart(fig)

def agg_tran_quater_amount(dfv, state, years): # AMOUNT PIE CHART QUARTERLY
    AT1 = dfv[dfv["Years"] == years]
    AT1.reset_index(drop = True, inplace = True)

    AT1G = AT1[AT1["State"] == state]
    AT1G.reset_index(drop = "index", inplace = True)

    AT1GG = AT1G.groupby("Quarter")[["Transaction_count", "Transaction_amount"]].sum()
    AT1GG.reset_index(inplace = True)

    A = state
    B = A.upper()
    fig = px.pie(AT1GG, names = "Quarter", values = "Transaction_amount", color = "Transaction_amount", hole = 0.4,
                 title = f"{B}'S {years} QAURTER WISE ANALYSIS", width = 470, height = 470)
    st.plotly_chart(fig)

# TRANSACTION TYPE ANALYSIS

def agg_tran_year_tt_tc(dfv, years, states): # COUNT PIE CHART YEARLY
    AT1 = dfv[dfv["Years"] == years]
    AT1.reset_index(drop = True, inplace = True)

    AT1G = AT1[AT1["State"] == states]
    AT1G.reset_index(drop = "index", inplace = True)

    AT1GG = AT1G.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    AT1GG.reset_index(inplace = True)

    C = states
    D = C.upper()

    fig = px.pie(AT1GG, names = "Transaction_type", values = "Transaction_count", color = "Transaction_type", 
                title = f"{D}'S {years} TRANSACTION TYPE WISE ANALYSIS", hole = 0.4, width = 470, height = 470)
    st.plotly_chart(fig)


def agg_tran_year_tt_ta(dfv, years, states):   # AMOUNT PIE CHART YEARLY 
    AT1 = dfv[dfv["Years"] == years]
    AT1.reset_index(drop = True, inplace = True)

    AT1G = AT1[AT1["State"] == states]
    AT1G.reset_index(drop = "index", inplace = True)

    AT1GG = AT1G.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    AT1GG.reset_index(inplace = True)

    C = states
    D = C.upper()

    fig1 = px.pie(AT1GG, names = "Transaction_type", values = "Transaction_amount", color = "Transaction_type", 
            title = f"{D}'S {years} TRANSACTION TYPE WISE ANALYSIS", hole = 0.4, width = 470, height = 470)

    st.plotly_chart(fig1)


def agg_tran_quarter_tt_tc(years, states, quarter):  # COUNT PIE CHART QUARTER
    AT1 = agg_tran[agg_tran["Years"] == years]
    AT1.reset_index(drop = True, inplace = True)

    AT1G = AT1[AT1["State"] == states]
    AT1G.reset_index(drop = "index", inplace = True)
    
    ATI = AT1G[AT1G["Quarter"] == quarter]
    ATI.reset_index(drop = "index", inplace = True)
    
    AT1GG = ATI.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    AT1GG.reset_index(inplace = True)

    C = states
    D = C.upper() 

    fig = px.pie(AT1GG, names = "Transaction_type", values = "Transaction_count", color = "Transaction_type", 
                 title = f"{D}'S {years} Q{quarter} TRANSACTION TYPE WISE ANALYSIS", hole = 0.4,
                 width = 470, height = 470)
    st.plotly_chart(fig)


def agg_tran_quarter_tt_ta(years, states, quarter): # AMOUNT PIE CHART QUARTER
    AT1 = agg_tran[agg_tran["Years"] == years]
    AT1.reset_index(drop = True, inplace = True)

    AT1G = AT1[AT1["State"] == states]
    AT1G.reset_index(drop = "index", inplace = True)
    
    ATI = AT1G[AT1G["Quarter"] == quarter]
    ATI.reset_index(drop = "index", inplace = True)
    
    AT1GG = ATI.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    AT1GG.reset_index(inplace = True)

    C = states
    D = C.upper() 

    fig = px.pie(AT1GG, names = "Transaction_type", values = "Transaction_amount", color = "Transaction_type", 
                 title = f"{D}'S {years} Q{quarter} TRANSACTION TYPE WISE ANALYSIS", hole = 0.4,
                 width = 470, height = 470)
    st.plotly_chart(fig)

# AGGREGATE USER ANALYSIS
    
def agg_user_year_brands(dfv, years):     # YEARLY USER BY BRANDS
    AU1 = dfv[dfv["Years"] == years]
    AU1.reset_index(drop = "index", inplace = True)

    AU1G = pd.DataFrame(AU1.groupby("Brands")["Transaction_count"].sum())
    AU1G.reset_index(inplace = True)

    fig = px.bar(AU1G, x = "Brands", y= "Transaction_count", color = "Brands", 
                title = f"{years} TRANSACTION ANALYSIS BY BRANDS",
                height = 550, width = 900)
    st.plotly_chart(fig)

def agg_user_year_quarter_brands(dfv, years, quarter):  # QUARTERLY OF EACH YEAR BY 
    AU1 = dfv[dfv["Years"] == years]
    AU1.reset_index(drop = "index", inplace = True)

    AUG1 = AU1[AU1["Quarter"] == quarter]
    AUG1.reset_index(drop = "index", inplace = True)

    AU1G = pd.DataFrame(AUG1.groupby("Brands")["Transaction_count"].sum())
    AU1G.reset_index(inplace = True)

    if years == 2022 and quarter !=1:
        st.write(":rainbow[NO DATA AVAILABLE IN THIS QUARTER]")
    else:
        fig = px.bar(AU1G, x = "Brands", y= "Transaction_count", color = "Brands", 
                    title = f"{years} Q{quarter} ANALYSIS BY BRANDS",
                    height = 550, width = 900)
        st.plotly_chart(fig)

# STATE WISE BRAND ANALYSIS

def agg_user_year_state_brands(dfv, years, state):
    AU1 = dfv[dfv["Years"] == years]
    AU1.reset_index(drop = "index", inplace = True)

    AUG1 = AU1[AU1["State"] == state]
    AUG1.reset_index(drop = "index", inplace = True)

    AU1G = pd.DataFrame(AUG1.groupby("Brands")["Transaction_count"].sum())
    AU1G.reset_index(inplace = True)

    fig = px.bar(AU1G, x = "Brands", y= "Transaction_count", color = "Brands", height = 550, width = 900, 
                title = f"{state.upper()}'S {years} ANALYSIS BY BRANDS")
    st.plotly_chart(fig)

# STATE WISE QUARTERLY BRAND ANALYSIS 
    
def agg_user_quarter_brands(dfv, years, state, quarter):

    AU2 = dfv[dfv["Years"] == years]
    AU2.reset_index(drop = "index", inplace = True)

    AU22 = AU2[AU2["State"] == state]
    AU22.reset_index(drop = "index", inplace = True)

    AU23 = AU22[AU22["Quarter"] == quarter]
    AU23.reset_index(drop = "index", inplace = True)

    if years == 2022 and quarter != 1:
        st.write(":rainbow[NO DATA AVAILABLE IN THIS QUARTER]")
    else:
        fig = px.bar(AU23, x = "Brands", y= "Transaction_count", color = "Brands", 
                     height = 550, width = 900, hover_data = "Percentages",
                     title = f"Q{quarter} OF {state.upper()}'S {years} ANALYSIS BY BRANDS")
        st.plotly_chart(fig)

# MAP TRANSACTION 

def map_tran_district_yearly_tc(dfv, state, year):  # DISTRICT WISE TC YEARLY ANALYSIS
    MT = dfv[dfv["Years"] == year]
    MT.reset_index(drop = True, inplace= True)

    MT1 = MT[MT["State"] == state]
    MT1. reset_index(drop = True, inplace = True)
    
    MT2 = MT1.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    MT2.reset_index(inplace = True)
    
    fig =px.bar(MT2, x = "Districts", y = "Transaction_count", color = "Districts", 
                title = f"DISTRICT WISE ANALYSIS OF YEAR {year}", height = 750, width = 1000)
    st.plotly_chart(fig)

def map_tran_district_yearly_ta(dfv, state, year):  # DISTRICT WISE TA YEARLY ANALYSIS
    MT = dfv[dfv["Years"] == year]
    MT.reset_index(drop = True, inplace= True)

    MT1 = MT[MT["State"] == state]
    MT1. reset_index(drop = True, inplace = True)
    
    MT2 = MT1.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    MT2.reset_index(inplace = True)
    
    fig =px.bar(MT2, x = "Districts", y = "Transaction_amount", color = "Districts", 
                title = f"DISTRICT WISE ANALYSIS OF YEAR {year}", height = 750, width = 1000)
    st.plotly_chart(fig)

def map_tran_district_quaterly_tc(dfv, state, year, quarter): # DISTRICT WISE TC QUARTERLY ANALYSIS
    MT = dfv[dfv["Years"] == year]
    MT.reset_index(drop = True, inplace= True)

    MT1 = MT[MT["State"] == state]
    MT1.reset_index(drop = True, inplace = True)
    
    MT2 = MT1[MT1["Quarter"] == quarter]
    MT2.reset_index(drop = True, inplace = True)

    MT3 = MT2.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    MT3.reset_index(inplace = True)

    fig = px.bar(MT3, x = "Districts", y = "Transaction_count", color = "Districts",
                 title = f"{state.upper()}'S Q{quarter} OF YEAR {year} DISTRICT WISE ANALYSIS", height = 750, width = 1000)
    st.plotly_chart(fig)
    
def map_tran_district_quaterly_ta(dfv, state, year, quarter):  # DISTRICT WISE TA QUARTERLY ANALYSIS
    MT = dfv[dfv["Years"] == year]
    MT.reset_index(drop = True, inplace= True)

    MT1 = MT[MT["State"] == state]
    MT1.reset_index(drop = True, inplace = True)
    
    MT2 = MT1[MT1["Quarter"] == quarter]
    MT2.reset_index(drop = True, inplace = True)

    MT3 = MT2.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    MT3.reset_index(inplace = True)

    fig = px.bar(MT3, x = "Districts", y = "Transaction_amount", color = "Districts",
                 title = f"{state.upper()}'S Q{quarter} OF YEAR {year} DISTRICT WISE ANALYSIS", height = 750, width = 1000)
    st.plotly_chart(fig)

def map_user_year_ru(dfv, years):     # YEARLY REGISTERED USER 
    MU1 = dfv[dfv["Years"] == years]
    MU1.reset_index(drop = "index", inplace = True)

    MU1G = MU1.groupby("State")[["Registered_users", "App_opens"]].sum()
    MU1G.reset_index(inplace = True)

    fig = px.bar(MU1G, x = "State", y= "Registered_users", color = "State", 
                hover_data = "App_opens", title = f"REGISTERED USER IN {years}",
                height = 700, width = 1000)
    st.plotly_chart(fig)

def map_user_quarter_ru(dfv, years, quarter):     # QUARTERLY REGISTERED USER 
    MU1 = dfv[dfv["Years"] == years]
    MU1.reset_index(drop = "index", inplace = True)

    MU1G = MU1[MU1["Quarter"] == quarter]
    MU1G.reset_index(drop = True, inplace = True)

    MUG1 = MU1G.groupby("State")[["Registered_users", "App_opens"]].sum()
    MUG1.reset_index(inplace = True)
    
    fig = px.bar(MUG1, x = "State", y= "Registered_users", color = "State", hover_data = "App_opens",
            title = f"{years} REGISTERED USER IN Q{quarter}",
            height = 700, width = 1000)
    st.plotly_chart(fig)

def map_user_year_state_ru(dfv, years, state): # DISTRICT WISE YEARLY REGISTERD USERS 
    MU1 = dfv[dfv["Years"] == years]
    MU1.reset_index(drop = "index", inplace = True)

    MUG1 = MU1[MU1["State"] == state]
    MUG1.reset_index(drop = "index", inplace = True)

    MU1G = MUG1.groupby("Districts")[["Registered_users", "App_opens"]].sum()
    MU1G.reset_index(inplace = True)

    fig = px.bar(MU1G, x = "Districts", y= "Registered_users", color = "Districts", height = 700, width = 1000,  
                hover_data = "App_opens", title = f"{state.upper()}'S REGISTERED USER IN {years}")
    st.plotly_chart(fig)

def map_user_quarter_state_ru(dfv, years, state, quarter): # DISTRICT WISE QUARTERLY REGISTERD USERS 

    MU2 = dfv[dfv["Years"] == years]
    MU2.reset_index(drop = "index", inplace = True)

    MU22 = MU2[MU2["State"] == state]
    MU22.reset_index(drop = "index", inplace = True)

    MU23 = MU22[MU22["Quarter"] == quarter]
    MU23.reset_index(drop = "index", inplace = True)

    fig = px.bar(MU23, x = "Districts", y= "Registered_users", color = "Districts", 
                    height = 700, width = 1000, hover_data = "App_opens",
                    title = f"{state.upper()}'S REGISTERED USER IN {years} OF Q{quarter}")
    st.plotly_chart(fig)

# TOP TRANSACTION
    
def top_tran_yearly_pincodes_tc(dfv, years, state):
    TU2 = dfv[dfv["Years"] == years]
    TU2.reset_index(drop = "index", inplace = True)

    TU22 = TU2[TU2["State"] == state]
    TU22.reset_index(drop = "index", inplace = True)

    TU23 = TU22.groupby(["Quarter", "Pincodes"])[["Transaction_count", "Transaction_amount"]].sum()
    TU23.reset_index(inplace  = True)
    
    fig = px.bar(TU23, x = "Quarter", y ="Transaction_count", hover_data = "Pincodes", color_discrete_sequence = ["orange"]*len(TU23), 
                 title = f"PINCODE WISE {state.upper()}'S TRANSACTION COUNT IN {years}",
                 height = 700, width = 900)
    st.plotly_chart(fig)

def top_tran_yearly_pincodes_ta(dfv, years, state):
    TU2 = dfv[dfv["Years"] == years]
    TU2.reset_index(drop = "index", inplace = True)

    TU22 = TU2[TU2["State"] == state]
    TU22.reset_index(drop = "index", inplace = True)

    TU23 = TU22.groupby(["Quarter", "Pincodes"])[["Transaction_count", "Transaction_amount"]].sum()
    TU23.reset_index(inplace  = True)
    
    fig = px.bar(TU23, x = "Quarter", y ="Transaction_amount", hover_data = "Pincodes", color_discrete_sequence = ["yellow"]*len(TU23),              
                 title = f"PINCODE WISE {state.upper()}'S TRANSACTION AMOUNT IN {years}",
                 height = 700, width = 900)
    st.plotly_chart(fig)

# TOP USER 

def top_user_yearly_pincodes_ru(dfv, years, state):
    TU2 = dfv[dfv["Years"] == years]
    TU2.reset_index(drop = "index", inplace = True)

    TU22 = TU2[TU2["State"] == state]
    TU22.reset_index(drop = "index", inplace = True)

    TU23 = pd.DataFrame(TU22.groupby(["Quarter", "Pincodes"])["Registered_users"].sum())
    TU23.reset_index(inplace  = True)
    
    fig = px.bar(TU23, x = "Quarter", y ="Registered_users", hover_data = "Pincodes", color_discrete_sequence = ["orange"]*len(TU23), 
                 title = f"PINCODE WISE {state.upper()}'S REGISTERED USERS IN {years}",
                 height = 700, width = 900)
    st.plotly_chart(fig)

#OVER ALL ANALYSIS
    
def top_least_tran_count(dfv):
    
    st.subheader(":orange[TOP 10 ANALYSIS]")

    Query1 = f'''select State, sum(Transaction_count) as transaction_count, sum(Transaction_amount) as transaction_count 
                 from {dfv} group by State order by transaction_count desc limit 10'''

    cursor.execute(Query1)
    Q1 = cursor.fetchall()
    connection.commit()

    df1 = pd.DataFrame(Q1, columns = ["STATE", "TRANSACTION COUNT", "TRANSACTION AMOUNT"])
    fig1 = px.bar(df1, x = "STATE", y = "TRANSACTION COUNT", hover_data = "TRANSACTION AMOUNT", color = "STATE", 
                title = "TOP 10 TRANSACTION COUNT", text_auto = True,
                height = 700, width = 900)
    st.plotly_chart(fig1)
    
    Query2 = f'''select State, sum(Transaction_count) as transaction_count, sum(Transaction_amount) as transaction_count 
                 from {dfv} group by State order by transaction_count asc limit 10'''

    cursor.execute(Query2)
    Q2 = cursor.fetchall()
    connection.commit()

    df2 = pd.DataFrame(Q2, columns = ["STATE", "TRANSACTION COUNT", "TRANSACTION AMOUNT"])
    fig2 = px.bar(df2, x = "STATE", y = "TRANSACTION COUNT", hover_data = "TRANSACTION AMOUNT", color = "STATE", 
                title = "LEAST 10 TRANSACTION COUNT", text_auto = True,
                height = 700, width = 900)
    st.plotly_chart(fig2)

def top_least_tran_amount(dfv):
    Query3 = f'''select State, sum(Transaction_count) as transaction_count, sum(Transaction_amount) as transaction_amount 
                  from {dfv} group by State order by transaction_amount desc limit 10'''

    cursor.execute(Query3)
    Q3 = cursor.fetchall()
    connection.commit()

    df3 = pd.DataFrame(Q3, columns = ["STATE", "TRANSACTION COUNT", "TRANSACTION AMOUNT"])
    fig3 = px.bar(df3, x = "STATE", y = "TRANSACTION AMOUNT", hover_data = "TRANSACTION COUNT", color = "STATE", 
                title = "TOP 10 TRANSACTION AMOUNT", text_auto = True,
                height = 700, width = 900)
    st.plotly_chart(fig3)

    Query4 = f'''select State, sum(Transaction_count) as transaction_count, sum(Transaction_amount) as transaction_amount 
                 from {dfv} group by State order by transaction_amount asc limit 10'''

    cursor.execute(Query4)
    Q4 = cursor.fetchall()
    connection.commit()

    df4 = pd.DataFrame(Q4, columns = ["STATE", "TRANSACTION COUNT", "TRANSACTION AMOUNT"])
    fig4 = px.bar(df4, x = "STATE", y = "TRANSACTION AMOUNT", hover_data = "TRANSACTION COUNT", color = "STATE", 
                title = "LEAST 10 TRANSACTION AMOUNT", text_auto = True,
                height = 700, width = 900)
    st.plotly_chart(fig4)
    
def top_least_ttype_amount():
    Query5 = f'''select state, transaction_type, sum(Transaction_count) as transaction_count, sum(Transaction_amount) as transaction_amount 
                from agg_transaction group by state, transaction_type order by transaction_amount desc limit 10'''

    cursor.execute(Query5)
    Q5 = cursor.fetchall()
    connection.commit()

    df5 = pd.DataFrame(Q5, columns = ["STATE", "TRAN_TYPE", "TRANSACTION COUNT", "TRANSACTION AMOUNT"])
    fig5 = px.bar(df5, x = "STATE", y= "TRANSACTION AMOUNT", color = "TRAN_TYPE", 
                title = "TOP 10 TRANSACTION AMOUNT BY TRANSACTION TYPE ", text_auto = True,
                height = 700, width = 900)
    st.plotly_chart(fig5)

    Query6 = f'''select state, transaction_type, sum(Transaction_count) as transaction_count, sum(Transaction_amount) as transaction_amount 
                from agg_transaction group by state, transaction_type order by transaction_amount asc limit 10'''

    cursor.execute(Query6)
    Q6 = cursor.fetchall()
    connection.commit()

    df6 = pd.DataFrame(Q6, columns = ["STATE", "TRAN_TYPE", "TRANSACTION COUNT", "TRANSACTION AMOUNT"])
    fig6 = px.bar(df6, x = "STATE", y= "TRANSACTION AMOUNT", hover_data = "TRANSACTION COUNT", color = "TRAN_TYPE", 
                title = "LEAST 10 TRANSACTION AMOUNT BY TRANSACTION TYPE", text_auto = True,
                height = 700, width = 900)
    st.plotly_chart(fig6)

def top_least_brands_count():
    Query7 = f'''select State, Brands, sum(Transaction_count) as transaction_count from agg_user 
                group by State, Brands order by transaction_count desc limit 10'''

    cursor.execute(Query7)
    Q7 = cursor.fetchall()
    connection.commit()

    df7 = pd.DataFrame(Q7, columns = ["STATE", "BRANDS", "TRANSACTION COUNT"])
    fig7 = px.bar(df7, x = "STATE", y= "TRANSACTION COUNT", color = "BRANDS", 
                title = "TOP 10 TRANSACTION COUNT BY BRANDS", text_auto = True,
                height = 700, width = 900)
    st.plotly_chart(fig7)

    Query8 = f'''select State, Brands, sum(Transaction_count) as transaction_count from agg_user 
                group by State, Brands order by transaction_count asc limit 10'''

    cursor.execute(Query8)
    Q8 = cursor.fetchall()
    connection.commit()

    df8 = pd.DataFrame(Q8, columns = ["STATE", "BRANDS", "TRANSACTION COUNT"])
    fig8 = px.bar(df8, x = "STATE", y = "TRANSACTION COUNT", color = "BRANDS", 
                title = "LEAST 10 TRANSACTION COUNT BY BRANDS", text_auto = True,
                height = 700, width = 900)
    st.plotly_chart(fig8)

def top_least_district_registered_users():
    Query9 = '''select State, Districts, sum(Registered_users) as registered_users from map_user 
                group by State, Districts order by registered_users desc limit 10'''

    cursor.execute(Query9)
    Q9 = cursor.fetchall()
    connection.commit()

    df9 = pd.DataFrame(Q9, columns = ["STATE", "DISTRICTS", "REGISTERED USERS"])
    fig9 = px.bar(df9, x = "DISTRICTS", y = "REGISTERED USERS", hover_data = "STATE", color = "STATE", 
                title = "TOP 10 REGISTERED USERS BY DISTRICT", text_auto = True,
                height = 700, width = 900)
    st.plotly_chart(fig9)
    

    Query10 = '''select State, Districts, sum(Registered_users) as registered_users from map_user 
                group by State, Districts order by registered_users asc limit 10'''

    cursor.execute(Query10)
    Q10 = cursor.fetchall()
    connection.commit()

    df10 = pd.DataFrame(Q10, columns = ["STATE", "DISTRICTS", "REGISTERED USERS"])
    fig10 = px.bar(df10, x = "DISTRICTS", y = "REGISTERED USERS", hover_data = "STATE", color = "STATE", 
                title = "LEAST 10 REGISTERED USERS BY DISTRICT", text_auto = True,
                height = 700, width = 900)
    st.plotly_chart(fig10)

def top_least_pincode_registered_users():
    Query11 = '''select State, Pincodes, sum(Registered_users) as registered_users from top_user 
                group by State, Pincodes order by registered_users desc limit 10'''

    cursor.execute(Query11)
    Q11 = cursor.fetchall()
    connection.commit()

    df11 = pd.DataFrame(Q11, columns = ["STATE", "PINCODES", "REGISTERED USERS"])
    fig11 = px.bar(df11, x = "STATE", y = "REGISTERED USERS", hover_data = "PINCODES", color = "STATE", 
                title = "TOP 10 REGISTERED USERS BY PINCODES", text_auto = True,
                height = 700, width = 900)
    st.plotly_chart(fig11)

    Query12 = '''select State, Pincodes, sum(Registered_users) as registered_users from top_user 
                group by State, Pincodes order by registered_users asc limit 10'''

    cursor.execute(Query12)
    Q12 = cursor.fetchall()
    connection.commit()

    df12 = pd.DataFrame(Q12, columns = ["STATE", "PINCODES", "REGISTERED USERS"])
    fig12 = px.bar(df12, x = "STATE", y = "REGISTERED USERS", hover_data = "PINCODES", color = "STATE", 
                title = "LEAST 10 REGISTERED USERS BY PINCODES", text_auto = True,
                height = 700, width = 900)
    st.plotly_chart(fig12)

# CONNECTING TO STREAMLIT
st.set_page_config(layout = "wide")
st.title(":green[PHONEPE DATA VISUALIZATION AND EXPLORATION]")

with st.sidebar:            
    SB = st.selectbox(":green[SELECT THE FILE TYPE]",
                 options = ["AGGREGATE", "MAP", "TOP", "OVERALL ANALYSIS"])
    

if SB == "AGGREGATE":
    SB1 = st.selectbox(":blue[SELECT THE TRANSACTION TYPE]",
            options = ["TRANSACTION","USER"])
    
    # AGGREGATE TRANSACTION CHART
    if SB1 == "TRANSACTION":
        MAP1 = st.selectbox(":rainbow[SELECT THE CHART TYPE]",
                    options = ["BAR CHART", "CHOROPLETH MAP"])
        if MAP1 == "BAR CHART":
            col1, col2 = st.columns(2)
            with col1:
                TC = st.selectbox(":red[SELECT FILE]",
                                options = ["TRANSACTION COUNT", "TRANSACTION AMOUNT"])
            with col2:
                year = st.selectbox(":red[SELECT YEAR]", agg_tran["Years"].unique())
            if TC == "TRANSACTION COUNT":
                agg_tran_year_count(agg_tran, year)

            elif TC == "TRANSACTION AMOUNT":
                agg_tran_year_amount(agg_tran, year)
            
        elif MAP1 == "CHOROPLETH MAP":
            col1, col2 = st.columns(2)
            with col1:
                SB4 = st.selectbox(":red[SELECT FILE]", 
                            options = ["TRANSACTION COUNT", "TRANSACTION AMOUNT"])
            with col2:
                SB5 = st.selectbox(":red[SELECT YEAR]", options = agg_tran["Years"].unique())    
            
            if SB4 == "TRANSACTION COUNT":
                choropleth_map_count(agg_tran, SB5)
            
            elif SB4 == "TRANSACTION AMOUNT":
                choropleth_map_amount(agg_tran, SB5)
        
        st.markdown(":orange[QUARTERLY TRANSACTION COUNT & AMOUNT OF EACH YEAR]")    

        col1, col2 = st.columns(2)  # QUARTER WISE ANALYSIS OF TC AND TA

        with col1:
            SB6 = st.selectbox(":red[SELECT THE STATE]", agg_tran["State"].unique())

        with col2:
            SB7 = st.selectbox(":red[SELECT THE YEAR]", agg_tran["Years"].unique())
            
        colm1, colm2 = st.columns(2)

        with colm1:
            st.markdown(":blue[TRANSACTION COUNT]")
            agg_tran_quater_count(agg_tran, SB6, SB7)

        with colm2:
            st.markdown(":blue[TRANSACTION AMOUNT]")
            agg_tran_quater_amount(agg_tran, SB6, SB7)
    
        st.markdown(":orange[TRANSACTION TYPE YEARLY ANALYSIS]") # TRANSACTION TYPE YEARLY ANALYSIS
        
        col11, col12 = st.columns(2)

        with col11:
            SB8 = st.selectbox(":green[SELECT STATE]", agg_tran["State"].unique())

        with col12:
            SB9 = st.selectbox(":green[ SELECT YEAR]", agg_tran["Years"].unique())

        co11, co12 = st.columns(2)

        with co11:
            st.markdown(":blue[TRANSACTION COUNT]")
            agg_tran_year_tt_tc(agg_tran, SB9, SB8)

        with co12:
            st.markdown(":blue[TRANSACTION AMOUNT]")
            agg_tran_year_tt_ta(agg_tran, SB9, SB8)

        st.markdown(":orange[TRANSACTION TYPE QUARTERLY ANALYSIS]") # TRANSACTION TYPE QUARTERLY ANALYSIS

        co1, co2, co3 = st.columns(3)

        with co1:
            SB10 = st.selectbox(":green[SELECT THE STATE]", agg_tran["State"].unique())

        with co2:
            SB11 = st.selectbox(":green[SELECT THE YEAR]", agg_tran["Years"].unique())

        with co3:
            SB12 = st.selectbox(":green[SELECT QUARTER]", agg_tran["Quarter"].unique())

        co111, co112 = st.columns(2)

        with co111:
            st.markdown(":blue[TRANSACTION COUNT]")
            agg_tran_quarter_tt_tc(SB11, SB10, SB12)

        with co112:
            st.markdown(":blue[TRANSACTION AMOUNT]")
            agg_tran_quarter_tt_ta(SB11, SB10, SB12)

    elif SB1 == "USER":
        st.markdown(":blue[TRANSACTION COUNT ANALYSIS]")
        st.markdown(":orange[YEARLY ANALYSIS]")

        co6, co7 = st.columns(2)
       
        with co6:
            SB13 = st.selectbox(":red[SELECT THE YEAR]", agg_user["Years"].unique())
        
        agg_user_year_brands(agg_user, SB13)

        st.markdown(":orange[QUARTERLY ANALYSIS]")
        
        co4, co5 = st.columns(2)

        with co4:
            SB14 = st.selectbox(":red[SELECT YEAR]", agg_user["Years"].unique())

        with co5:
            SB15 = st.selectbox(":red[SELECT QUARTER]", agg_user["Quarter"].unique())
        
        agg_user_year_quarter_brands(agg_user,SB14, SB15)

        st.markdown(":orange[STATE WISE YEARLY ANALYSIS]")

        co8, co9 =st.columns(2)

        with co8:
            SB16 = st.selectbox(":green[SELECT THE STATE]", agg_user["State"].unique())

        with co9:
            SB17 = st.selectbox(":green[SELECT THE YEAR]", agg_user["Years"].unique())

        agg_user_year_state_brands(agg_user,SB17, SB16)
        
        st.markdown(":orange[STATE WISE QUARTERLY OF EACH YEAR ANALYSIS]")

        co10, co11, co12 = st.columns(3)

        with co10:
            SB18 = st.selectbox(":green[STATE]", agg_user["State"].unique())

        with co11:
            SB19 = st.selectbox(":green[YEAR]", agg_user["Years"].unique())

        with co12:
            SB20 = st.selectbox(":green[QUARTER]", agg_user["Quarter"].unique())

        agg_user_quarter_brands(agg_user, SB19, SB18, SB20)

    else:
        pass

elif SB == "MAP":
    SB2 = st.selectbox(":blue[SELECT THE TRANSACTION TYPE]",
                options = ["TRANSACTION","USER"])
    
    if SB2 == "TRANSACTION":
        MAP2 = st.selectbox(":rainbow[SELECT THE CHART TYPE]",
                    options = ["BAR CHART", "CHOROPLETH MAP"])
        if MAP2 == "BAR CHART":
            cl1, cl2 = st.columns(2)
            
            with cl1:
                TC1 = st.selectbox(":red[SELECT FILE]",
                                options = ["TRANSACTION COUNT", "TRANSACTION AMOUNT"])
            with cl2:
                year = st.selectbox(":red[SELECT YEAR]", map_tran["Years"].unique())
            if TC1 == "TRANSACTION COUNT":
                agg_tran_year_count(map_tran, year)

            elif TC1 == "TRANSACTION AMOUNT":
                agg_tran_year_amount(map_tran, year)

        elif MAP2 == "CHOROPLETH MAP":
            cll1, cll2 = st.columns(2)
            with cll1:
                SB21 = st.selectbox(":red[SELECT FILE]", 
                            options = ["TRANSACTION COUNT", "TRANSACTION AMOUNT"])
            with cll2:
                SB22 = st.selectbox(":red[SELECT YEAR]", map_tran["Years"].unique())    
            
            if SB21 == "TRANSACTION COUNT":
                choropleth_map_count(map_tran, SB22)
            
            elif SB21 == "TRANSACTION AMOUNT":
                choropleth_map_amount(map_tran, SB22)

        st.markdown(":orange[QUARTERLY TRANSACTION COUNT & AMOUNT OF EACH YEAR]")

        cl3, cl4 = st.columns(2)  # QUARTER WISE ANALYSIS OF TC AND TA

        with cl3:
            SB23 = st.selectbox(":red[SELECT THE STATE]", map_tran["State"].unique())

        with cl4:
            SB24 = st.selectbox(":red[SELECT THE YEAR]", map_tran["Years"].unique())
            
        cl5, cl6 = st.columns(2)
        
        with cl5:
            st.markdown(":blue[TRANSACTION COUNT]")
            agg_tran_quater_count(map_tran, SB23, SB24)

        with cl6:
            st.markdown(":blue[TRANSACTION AMOUNT]")
            agg_tran_quater_amount(map_tran, SB23, SB24)

        st.markdown(":orange[DISTRICT WISE YEARLY ANALYSIS]")

        TC3 = st.selectbox(":red[SELECT THE TRANSACTION TYPE]", 
                           options = ["TRANSACTION COUNT", "TRANSACTION AMOUNT"])
        
        cl15, cl16 = st.columns(2)

        with cl15:
            SB29 = st.selectbox(":green[SELECT THE STATE]", map_tran["State"].unique())

        with cl16:
            SB30 = st.selectbox(":green[SELECT THE YEAR]", map_tran["Years"].unique())

        if TC3 == "TRANSACTION COUNT":
            st.write(":rainbow[TRANSACTION COUNT]")
            map_tran_district_yearly_tc(map_tran, SB29, SB30)
            
        
        elif TC3 == "TRANSACTION AMOUNT":
            st.write(":rainbow[TRANSACTION AMOUNT]")
            map_tran_district_yearly_ta(map_tran, SB29,SB30)

        st.markdown(":orange[DISTRICT WISE QUARTERLY ANALYSIS]")

        TC4 = st.selectbox(":red[TRANSACTION TYPE]", 
                           options = ["TRANSACTION COUNT", "TRANSACTION AMOUNT"])
        
        cl17, cl18, Cl19 = st.columns(3)

        with cl17:
            SB31 = st.selectbox(":green[STATE]", map_tran["State"].unique())

        with cl18:
            SB32 = st.selectbox(":green[YEAR]", map_tran["Years"].unique())
        
        with Cl19:
            SB33 = st.selectbox(":green[QUARTER]", map_tran["Quarter"].unique())

        if TC4 == "TRANSACTION COUNT":
            st.write(":rainbow[TRANSACTION COUNT]")
            map_tran_district_quaterly_tc(map_tran, SB31, SB32, SB33)

        elif TC4 == "TRANSACTION AMOUNT":
            st.write(":rainbow[TRANSACTION COUNT]")
            map_tran_district_quaterly_ta(map_tran, SB31, SB32, SB33)
        
    elif SB2 == "USER":
        st.markdown(":blue[REGISTERED USERS ANALYSIS]")
        st.markdown(":orange[STATE WISE YEARLY ANALYSIS]")

        cl20, cl21 = st.columns(2)
       
        with cl20:
            SB34 = st.selectbox(":red[SELECT THE YEAR]", map_user["Years"].unique())
        map_user_year_ru(map_user, SB34)

        st.markdown(":orange[STATE WISE QUARTERLY ANALYSIS]")
        
        cl22, cl23 = st.columns(2)

        with cl22:
            SB35 = st.selectbox(":red[SELECT YEAR]", map_user["Years"].unique())

        with cl23:
            SB36 = st.selectbox(":red[SELECT QUARTER]", map_user["Quarter"].unique())
        
        map_user_quarter_ru(map_user,SB35, SB36)

        st.markdown(":orange[DISTRICT WISE YEARLY ANALYSIS]")

        cl24, cl25 =st.columns(2)

        with cl24:
            SB37 = st.selectbox(":green[SELECT THE STATE]", map_user["State"].unique())

        with cl25:
            SB38= st.selectbox(":green[SELECT THE YEAR]", map_user["Years"].unique())

        map_user_year_state_ru(map_user, SB38, SB37)

        st.markdown(":orange[DISTRICT WISE QUARTERLY ANALYSIS]")

        cl26, cl27, cl28 = st.columns(3)

        with cl26:
            SB39 = st.selectbox(":green[STATE]", map_user["State"].unique())

        with cl27:
            SB40 = st.selectbox(":green[YEAR]", map_user["Years"].unique())

        with cl28:
            SB41 = st.selectbox(":green[QUARTER]", map_user["Quarter"].unique())

        map_user_quarter_state_ru(map_user, SB40, SB39, SB41)

    else:
        pass

elif SB == "TOP":
    SB3 = st.selectbox(":blue[SELECT THE TRANSACTION TYPE]",
                options = ["TRANSACTION","USER"])
    
    if SB3 == "TRANSACTION":
        MAP3 = st.selectbox(":rainbow[SELECT THE CHART TYPE]",
                    options = ["BAR CHART", "CHOROPLETH MAP"])
        if MAP3 == "BAR CHART":
            cl7, cl8 = st.columns(2)
            
            with cl7:
                TC12 = st.selectbox(":red[SELECT FILE]",
                                options = ["TRANSACTION COUNT", "TRANSACTION AMOUNT"])
            with cl8:
                year = st.selectbox(":red[SELECT YEAR]", top_tran["Years"].unique())
            if TC12 == "TRANSACTION COUNT":
                agg_tran_year_count(top_tran, year)

            elif TC12 == "TRANSACTION AMOUNT":
                agg_tran_year_amount(top_tran, year)

        elif MAP3 == "CHOROPLETH MAP":
            cl9, cl10 = st.columns(2)
            with cl9:
                SB25 = st.selectbox(":red[SELECT FILE]", 
                            options = ["TRANSACTION COUNT", "TRANSACTION AMOUNT"])
            with cl10:
                SB26 = st.selectbox(":red[SELECT YEAR]", top_tran["Years"].unique())    
            
            if SB25 == "TRANSACTION COUNT":
                choropleth_map_count(top_tran, SB26)
            
            elif SB25 == "TRANSACTION AMOUNT":
                choropleth_map_amount(top_tran, SB26)

        st.markdown(":orange[QUARTERLY TRANSACTION COUNT & AMOUNT OF EACH YEAR]")

        cl11, cl12 = st.columns(2)  # QUARTER WISE ANALYSIS OF TC AND TA

        with cl11:
            SB27 = st.selectbox(":red[SELECT THE STATE]", top_tran["State"].unique())

        with cl12:
            SB28 = st.selectbox(":red[SELECT THE YEAR]", top_tran["Years"].unique())
            
        cl13, cl14 = st.columns(2)
        
        with cl13:
            st.markdown(":blue[TRANSACTION COUNT]")
            agg_tran_quater_count(top_tran, SB27, SB28)

        with cl14:
            st.markdown(":blue[TRANSACTION AMOUNT]")
            agg_tran_quater_amount(top_tran, SB27, SB28)

        st.markdown(":orange[PINCODE WISE TRANSACTION COUNT & AMOUNT]")

        NSB = st.selectbox(":red[SELECT THE TRANSACTION TYPE]", 
                           options = ["TRANSACTION COUNT", "TRANSACTION AMOUNT"])
        
        ncol1, ncol2 = st.columns(2)

        with ncol1:
            BS1 = st.selectbox(":green[SELECT THE STATE]", top_tran["State"].unique())

        with ncol2:
            BS2 = st.selectbox(":green[SELECT THE YEAR]", top_tran["Years"].unique())

        if NSB == "TRANSACTION COUNT":
            top_tran_yearly_pincodes_tc(top_tran, BS2, BS1)

        elif NSB == "TRANSACTION AMOUNT":
            top_tran_yearly_pincodes_ta(top_tran, BS2, BS1)
    
    
    elif SB3 == "USER":
        st.markdown(":orange[PINCODE WISE REGISTERED USERS]")

        ncol3, ncol4 = st.columns(2)

        with ncol3:
            BS3 = st.selectbox(":green[SELECT THE STATE]", top_user["State"].unique())

        with ncol4:
            BS4 = st.selectbox(":green[SELECT THE YEAR]", top_user["Years"].unique())

        top_user_yearly_pincodes_ru(top_user, BS4, BS3)
    else:
        pass

elif SB == "OVERALL ANALYSIS":
    OVA = st.selectbox(":rainbow[SELECT THE QUESTION]", 
                 options = ["1. Top 10 and Least 10 Transaction Count in Aggregate Transaction",

                            "2. Top 10 and Least 10 Transaction Count in Map Transaction", 

                            "3. Top 10 and Least 10 Transaction Count in Top Transaction",

                            "4. Top 10 and Least 10 Transaction Amount in Aggregate Transaction",

                            "5. Top 10 and Least 10 Transaction Amount in Map Transaction",

                            "6. Top 10 and Least 10 Transaction Amount in Top Transaction",

                            "7. Top 10 and Least 10 Transaction Amount by Transaction Type",

                            "8. Top 10 and Least 10 Transaction Count by Brands",

                            "9. Top 10 and Least 10 Registered users by District",

                            "10. Top 10 and Least 10 Registered users by Pincode"])
    

    
  
    if OVA == "1. Top 10 and Least 10 Transaction Count in Aggregate Transaction":
        top_least_tran_count("agg_transaction")

    elif OVA == "2. Top 10 and Least 10 Transaction Count in Map Transaction":
        top_least_tran_count("map_transaction")

    elif OVA == "3. Top 10 & Least 10 Transaction Count in Top Transaction":
        top_least_tran_count("top_transaction")

    elif OVA == "4. Top 10 and Least 10 Transaction Amount in Aggregate Transaction":
        top_least_tran_amount("agg_transaction")
    
    elif OVA == "5. Top 10 and Least 10 Transaction Amount in Map Transaction":
        top_least_tran_amount("map_transaction")

    elif OVA == "6. Top 10 and Least 10 Transaction Amount in Top Transaction":
        top_least_tran_amount("top_transaction")

    elif OVA == "7. Top 10 and Least 10 Transaction Amount by Transaction Type":
        top_least_ttype_amount()

    elif OVA == "8. Top 10 and Least 10 Transaction Count by Brands":
        top_least_brands_count()

    elif OVA == "9. Top 10 and Least 10 Registered users by District":
        top_least_district_registered_users()

    elif OVA == "10. Top 10 and Least 10 Registered users by Pincode":
        top_least_pincode_registered_users()
else:
    pass






