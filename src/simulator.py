# External imports
import pandas as pd

#===============================================================================
# Class for simulating strategies 
#===============================================================================

class Simulator:
	'''
	Class for simulating simplest trading strategies and their outcome
	'''
	def __init__(self, finance_data, depot, strategy):
		'''
		Constructor of the simulator class
		
		Args:
			finance_data (pd.DataFrame): data frame containing all the finance
				data on which the simulation is run
			depot (Depot object): contains the starting parameters for the
				simulation.
			strategy (function): the strategy used for buying and selling
		'''
		# Copy references to parameters to class variables
		self.finance = finance_data
		self.depot = depot
		self.strategy = strategy
		# Create sorted list of unique dates from given finance data
		self.dates = list(set(self.finance.data.reset_index()['Date']))
		self.dates.sort()
		# Create the simulation result object
		self.result = pd.DataFrame(index=self.dates)
		self.result['capital'] = pd.np.nan 
	
		
	def run(self, **kwargs):
		'''
		Function to run the simulation of a strategy
		'''
		# Initialize back-testing variables
		for time in self.dates:
			# only pass data that should be known
			time_data = self.finance.data.select(lambda x: x[1] <= time)
			self.strategy(data=time_data, depot=self.depot, time=time, **kwargs)
			# Save the time development of the capital
			self.result.loc[time]['capital'] = self.depot.capital
		# At end of simulation monetize all your assets at closing price
		time = max(self.dates)
		self.depot.monetize(self.finance.data.xs(time,level=1)['Close'])
		# Sace the capital in results object
		self.result.loc[time]['capital'] = self.depot.capital
		# For convenience return the result object
		return self.result
