# 🌍 GHG Emissions Calculator

A web application for calculating corporate Scope 1 and 
Scope 2 greenhouse gas emissions following the 
GHG Protocol Corporate Accounting and Reporting Standard.

## 🔗 Live Demo
[Open the calculator](your-streamlit-url-here)

## 📋 What it calculates

**Scope 1 — Stationary Combustion**
- Natural gas (MMBtu/year)
- Diesel (liters/year)
- Petrol (liters/year)
- LPG (liters/year)

**Scope 2 — Purchased Electricity (Location-Based)**
- 27 US grid subregions (EPA eGRID 2023)
- 4 GCC country and Pakistan grids (Ember Climate 2024/2025)

## 📊 Data Sources

| Source | Used for |
|--------|----------|
| EPA GHG Emission Factors Hub 2025 | Scope 1 emission factors |
| EPA eGRID 2023 | US electricity grid factors |
| Ember Climate 2024/2025 | GCC electricity grid factors |
| GHG Protocol Corporate Standard (2015) | Calculation methodology |

## 🔬 Methodology

**Scope 1** factors include CO2, CH4, and N2O converted 
to CO2e using IPCC AR5 GWPs (CH4=28, N2O=265).
Source: EPA GHG Emission Factors Hub 2025.

**Scope 2** uses location-based method per GHG Protocol 
Scope 2 Guidance (2015). Market-based method not included.

## ⚠️ Limitations

Covers stationary combustion (Scope 1) and purchased 
electricity (Scope 2) only. Not included:
- Mobile combustion (company vehicles)
- Fugitive emissions (refrigerants, leaks)
- Process emissions
- All 15 Scope 3 categories

## 🛠️ Tech Stack

Python | Streamlit | Pandas | Plotly Express

## 💻 Run locally

```bash
pip install streamlit pandas plotly openpyxl
streamlit run app.py
```

## 👤 Author

Built by [Sandarah Ashraf] — MS Environmental Engineering  
GitHub: https://github.com/sandarahashraf  
LinkedIn: [Sandarah Ashraf] (https://www.linkedin.com/in/sandarah-ashraf-80a8561b9/)