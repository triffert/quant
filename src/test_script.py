# External imports
import pandas as pd

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
END = '2015-11-01'

# Reload for edits in module financedata to take place
reload(fd)
# Load the first three DAX companies to F 
F = fd.FinanceData(name_list=fd.DAX[:1], start_date=START, end_date=END)

# Reload for edits in module depot to take place
reload(dp)
# Create a depot
D = dp.Depot(capital=10000, fees=1)

# Reload for edits in module simulator to take place
reload(sim)
reload(strat)
# Initiate simulator
S = sim.Simulator(finance_data=F, depot=D, strategy=strat.inter_day_even)
# Run simulator and plot result
S.run().plot()
