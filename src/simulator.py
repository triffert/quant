################################################################################
# A small script for playing around with the Yahoo-finance API
################################################################################
import pandas as pd

class Simulator:
	'''
	Class for simulating simplest trading strategies and their outcome
	'''
	def __init__(self, finance, depot):
		
		self.finance = finance
		# Create sorted date list from given data
		self.dates = list(set(self.finance.data.reset_index()['Date']))
		self.dates.sort()
	
		
	def run(self, strategy):
		# Initialize back-testing variables
		result = pd.DataFrame(index=self.dates)
		# Pretty sure there is a nicer way to initialize the data frame
		result['Bank'] = pd.np.nan
		bank = self.bankroll
		for time in self.dates:
			bank = strategy(
						bank=bank,
						data=self.finance.data, 
						portfolio=self.portfolio,
						time=time,
						stocks=self.stocks,
						fees=self.fees
					)
			result.loc[time]['Bank'] = bank
		# Return the time-line of the bank roll
		return result
	

