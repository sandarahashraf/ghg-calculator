#_________________________________________________________
# Scope 1 Emission Factors
# Source: EPA GHG Emission Factors Hub 2025
# Method: CO2 + (CH4 * 28) + (N2O * 265)
# GWPs : IPCC AR5 (CH4=28, N2O=265)
# Units : metric tons CO2e per unit of fuel
#_________________________________________________________

Scope1_Factors = {
    'Natural Gas' : 0.0531145,      # t CO2e per mmBtu
    'Diesel' :      0.00270583,     # t CO2e per Liter
    'Petrol':       0.00232784,     # t CO2e per Liter
    'LPG':          0.00150677      # t CO2e per Liter
}


#________________________________________________
# Scope 2  Electricity Emission Factors
# Source : Ember Yearly Electricity data 2024/2025
# Method : Generation-based electricity carbon intensity
# Units : metric tons CO2e per kWh
#________________________________________________

GCC_Factors = {
    'UAE National Grid':      0.000468,
    'Saudi Arabia Grid':      0.000692,
    'Qatar Grid':             0.000582,
    'Kuwait Grid':            0.000635,
    'Pakistan National Grid': 0.000308
}


#_________________________________________________
# SCOPE 1 FUNCTION
#_________________________________________________

def calculate_scope1 (natural_gas, diesel, petrol, lpg, factors):
    """
    Scope 1 stationary combustion 
    GHG Protocol Corporate Standard, Chapter 4

    natural_gas: consumption in MMBtu/Year
    diesel:      consumption in Liters/Year
    petrol:      consumption in Liters/Year
    lpg:         consumption in Liters/Year
    factors:     Scope1_Factors dictionary

    returns: breakdown dict + total in metric tons CO2e
    """
    gas_CO2e = natural_gas * factors['Natural Gas']
    diesel_CO2e = diesel * factors['Diesel']
    petrol_CO2e = petrol * factors['Petrol']
    lpg_CO2e = lpg * factors['LPG']

    total_CO2e = (gas_CO2e + diesel_CO2e + petrol_CO2e + lpg_CO2e)

    breakdown = {
        'Natural Gas': gas_CO2e,
        'Diesel':      diesel_CO2e,
        'Petrol':      petrol_CO2e,
        'LPG':         lpg_CO2e
        
    }
    return  breakdown, total_CO2e

#_________________________________________________
# SCOPE 2 FUNCTION
#_________________________________________________

def calculate_scope2_location (electricity_kwh, grid_region, target_columns  , gcc_factors):
    """
    Scope 2 location-based emissions
    GHG Protocol Scope 2 Guidance, Location-Based Method

    electricity_kwh: annual consumption in kWh
    grid_region: name of the electricity grid
    target_columns: required columns in the eGRID dataFrame
    gcc_factors: dictionary of GCC factors

    returns: emissions metric tons CO2e, factors used, source 
    """
    # Check GCC regions first
    if grid_region  in gcc_factors:
        factor = gcc_factors[grid_region]
        source = 'Ember Climate, Global Electricity Review 2024/2025'

    else:
       # Look up  US region in eGRID
       factor = float(target_columns.loc[target_columns['SRNAME'] == grid_region, 'CO2e_factor'].values[0])
       source = 'EPA eGRID 2023'
      
    emissions = electricity_kwh * factor

    return emissions, factor, source



