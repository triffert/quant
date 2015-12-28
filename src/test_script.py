# External imports
import pandas as pd
import importlib
# Local imports
import financedata as fd
import simulator as sim
import depot as dp
import strategies as strat

#===============================================================================
# This script can be run a standalone, but is mostly a code collection
#===============================================================================

# Define start and end date variables
START = '2013-11-01'
END = '2014-11-01'

# Reload for edits in module financedata to take place
importlib.reload(fd)
# Load the first three DAX companies to F 
F = fd.FinanceData(name_list=fd.DAX[:10], start_date=START, end_date=END)

# Reload for edits in module depot to take place
importlib.reload(dp)
# Create a depot
D = dp.Depot(capital=100000, fees=5)

# Build predictor
import statsmodels.formula.api as sm
result = sm.ols(formula="Between_Day_Rel ~ Open + High + Low + Close \
					+ Previous_Day_Rel_1 + Previous_Day_Rel_2 \
					+ Previous_Day_Rel_3",\
					data=F.data).fit()
result.summary()

# Plot relationship of data
F.data[['Between_Day_Rel','Within_Day_Rel']].dropna().plot(kind='density',xlim=[-0.02,0.02])
F.data[['Between_Day_Rel','Within_Day_Rel']].dropna().mean()

# Reload for edits in module simulator to take place
importlib.reload(sim)
importlib.reload(strat)
# Initiate simulator
S = sim.Simulator(finance_data=F, depot=D, strategy=strat.inter_day_even)
# Run simulator and plot result
S.run().plot()
