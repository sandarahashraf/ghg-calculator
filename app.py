import pandas as pd
import streamlit as st 
import plotly.express as px

from calculation import (Scope1_Factors, 
                        GCC_Factors,  
                        calculate_scope1, 
                        calculate_scope2_location
 )



st.set_page_config(page_title="GHG Calculator", page_icon="🌍", layout="wide")

@st.cache_data
def load_egrid(): 
   df_egrid = pd.read_excel('data/egrid2023_data_rev2.xlsx', sheet_name="SRL23", header=1)
   target_columns = df_egrid[['SUBRGN', 'SRNAME', 'SRCO2RTA']].copy()
   target_columns ['CO2e_factor'] = target_columns['SRCO2RTA'] * 0.00000045359
   return target_columns.dropna()

target_columns = load_egrid()


gcc_list = list(GCC_Factors.keys())
usa_list = list(target_columns['SRNAME'].unique())
all_regions = gcc_list + usa_list
 

st.title("🌍 GHG Emissions Calculator")
st.markdown(""" 
Calculates corporate greenhouse gas 
emissions based on the 
***GHG Protocol Corporate Standard***.
Enter facility data in the sidebar.
""")


st.sidebar.header("Enter Facility Data")

company = st.sidebar.text_input(
   "Company Name", 
   value= "My Company"
   )

year = st.sidebar.selectbox(
   "Reporting Year",
   [2025, 2024, 2023, 2022]
)

st.sidebar.markdown("---")
st.sidebar.subheader("🔥 Scope 1 - Fuels")

natural_gas = st.sidebar.number_input(
   "Natural Gas (MMBtu/Year)", 
   min_value=0.0, 
   value=10000.0
)

diesel = st.sidebar.number_input(
   "Diesel (Liters/Year)",
    min_value=0.0, 
    value=50000.0
)

petrol = st.sidebar.number_input(
   "Petrol (Liters/Year)",
    min_value=0.0, 
    value=0.0
)   

lpg = st.sidebar.number_input(
   "LPG (Liters/Year)",
    min_value=0.0, 
    value=0.0
)

st.sidebar.markdown("---")
st.sidebar.subheader("⚡ Scope 2 - Electricity")

electricity_kwh = st.sidebar.number_input(
   "Electricity (kWh/Year)",
   min_value=0.0,
   value=500000.0
)

grid_region = st.sidebar.selectbox(
   "Grid Region",
   all_regions
)

st.sidebar.markdown("---")
calculate = st.sidebar.button(
   "Calculate Emissions",
   type = "primary",
   use_container_width = True
   )

if calculate:
   breakdown, total_scope1 = calculate_scope1(natural_gas, diesel, petrol, lpg, Scope1_Factors)

   scope2, factor, source = calculate_scope2_location(electricity_kwh, grid_region, target_columns, GCC_Factors)

   total = total_scope1 + scope2

   st.markdown("---")
   st.subheader(f"📊 Results - {company} ({year})")

   col1, col2, col3 = st.columns(3)
   col1.metric(
   label=" 🔥 Scope 1",
   value=f"{total_scope1:,.1f} tCO2e"
   )
   col2.metric(
   label=" ⚡Scope 2",
   value=f"{scope2:,.1f} tCO2e"
   )

   col3.metric(
   label="🌍 Total",
   value=f"{total:,.1f} tCO2e"
)

   col_a, col_b = st.columns(2)
   with col_a:

      fig_1 = px.pie(
         values=[total_scope1, scope2],
         names=["Scope 1", "Scope 2"],
         title= "Scope 1 vs Scope 2",
         color_discrete_sequence= ['#FF6B6B', '#4ECDC4'],
         hole=0.3
      )
      st.plotly_chart(fig_1, use_container_width=True)
   

   with col_b:

      sources = list(breakdown.keys()) + ["Electricity"]
      values = list(breakdown.values()) + [scope2]
      scopes = ['Scope 1'] * len(breakdown) + ['Scope 2']


      fuel_df = pd.DataFrame({
         'Source': sources,
         'tCO2e': values,
         'Scope': scopes
     })

      fuel_df = fuel_df[fuel_df['tCO2e'] > 0]

      fig_2 = px.bar(
         fuel_df,
         x='Source',
         y='tCO2e',
         title="Emissions by Source",
         color='Scope',
         color_discrete_map={
            'Scope 1': '#FF6B6B', 
            'Scope 2': '#4ECDC4'
         }, 
         text = 'tCO2e'
      )
      fig_2.update_traces(
         texttemplate='%{text:,.1f}', 
         textposition='outside'
      )
      fig_2.update_layout(showlegend=True)
      st.plotly_chart(fig_2, use_container_width=True)

   st.markdown("---")
   st.info(f"""
   **Methodology** 

   **Scope 1 - Stationary Combustion**
   Emission factors from EPA GHG Emission Factors Hub 2025.
   Includes CO2, CH4, N2O converted to CO2e using IPCC AR5 GWPs
   (CH4 = 28, N2O = 265).

   **Scope 2 — Location-Based Method**
   Emission factor applied: **{factor:.6f} tCO2/kWh**
   Source: **{source}**
   Method: Location-based per GHG Protocol Scope 2 Guidance (2015).

   **Reporting Standard**
   GHG Protocol Corporate Accounting and Reporting Standard,
   Revised Edition (2015).
   """)

   st.warning("""
   **Limitations** 
   This calculator covers Scope 1 stationary combustion and 
   Scope 2 purchased electricity only.
   Not included: mobile combustion, fugitive emissions, 
   process emissions, and all 15 Scope 3 categories.
   """)
   
   st.success("✅ Calculation complete!")

else:
   st.info("👈 Enter data in the sidebar and click Calculate Emissions")
