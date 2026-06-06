import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st
import sqlite3 
from datetime import datetime
st.set_page_config(page_title="F1 Risk Interactive Dashboard", layout="wide")
st.title("Formula-1 Racing Contract Risk Analyzer")
st.image("https://www.racefans.net/wp-content/uploads/2024/03/racefansdotnet-7172831_HiRes.jpg",width=450)
st.write("This app can identify the probability of Risk on contract curcuit In Foremula- 1 Racing")

sql_conv=sqlite3.connect("f1_project.db")
query="SELECT*FROM risk_analysis"
Data=pd.read_sql_query(query,sql_conv)

Data["Contract ends"]=pd.to_numeric(Data['Contract ends'] ,errors='coerce')
con_end=Data["Contract ends"]

country_list=sorted(Data['country'].unique().tolist())
st.sidebar.header("Filter Option")
country=st.sidebar.selectbox("Enter your country ",country_list)



current_year= datetime.now().year
date=list(range(current_year,2060))
year=st.sidebar.selectbox("Enter Year",date)

filtered_data = Data[Data['country'] == country]
total_circuits=len(filtered_data)

risk=year
high_risk=filtered_data[filtered_data['Contract ends']<=risk]
if total_circuits>0:
    pro_risk=len(high_risk)/total_circuits
else:
    pro_risk=0.0

col1,col2,col3=st.columns(3)
col1.metric(f"Total Circuits ({country})", total_circuits)
col2.metric(f"High Risk (By {year})", len(high_risk))
col3.metric("Risk Percentage", f"{pro_risk:.1%}")
l_col1,l_col2 = st.columns(2)
with  l_col1:
    if total_circuits >0 and pro_risk >0:
        labels=["High Risk ", "SafeZone"]
        sizes=[pro_risk,1-pro_risk]
        colors=["Red","green"]
        plt.figure(figsize=(6,6))
        plt.pie(sizes,labels=labels,colors=colors,autopct="%1.1f%%",explode=(0.1,0) , wedgeprops={"linestyle":"--","linewidth":2,"edgecolor":"yellow"},shadow=True )
        plt.title(f"Chart show the risk analysis in circuits                    contrats({year})",fontsize=16,fontweight='bold')
        plt.axis("equal")
        st.pyplot(plt)
        st.success("Congrats ! You Successfully Print Chart")
    else:
        st.info(f"{country}'s contract has not expired yet in {year}, so the chart is empty.")
with l_col2:
    
    st.subheader(f"🚨 Expiring Tracks List (<= {year})")
    display_cols = [c for c in ['Grand Prix', 'Circuit', 'Contract ends', 'country'] if c in high_risk.columns]
    if len(high_risk) > 0:
        st.dataframe(high_risk[display_cols], use_container_width=True)
    else:
        st.success(f"Congrats! {year} is not expire till now.") 
