# External module imports
import yahoo_finance as yf
import pandas as pd

#===============================================================================
# Global module variables
#===============================================================================

# Start and end time for data collection used as default values
START = pd.to_datetime('2013-11-01')
END = pd.to_datetime('2014-11-01')

# All companies in the DAX
DAX = ['ADS.DE','ALV.DE','BAS.DE','BAYN.DE','BEI.DE','BMW.DE','CBK.DE',
		'CON.DE','DAI.DE','DB1.DE','DBK.DE','DPW.DE','DTE.DE','EOAN.DE',
		'FME.DE','FRE.DE','HEI.DE','HEN3.DE','IFX.DE','LHA.DE','LIN.DE',
		'LXS.DE','MRK.DE','MUV2.DE','RWE.DE','SAP.DE','SDF.DE','SIE.DE',
		'TKA.DE','VOW3.DE']

#===============================================================================
# Class for finance Data 
#===============================================================================

class FinanceData:
	'''
	Class containing financial data, loading, cleaning and enriching functions 
	'''
		
	def __init__(self, name_list, start_date=START,	end_date=END):
		'''
		Constructor
		'''
		# Copy the parameters to class variables
		self.name_list = name_list
		self.start_date = start_date
		self.end_date = end_date
		# Create empty data frame for containing the finance data
		self.data = pd.DataFrame()
		# Load the data
		self.load_data()
		# Enrich the data
		self.enrich_data()
		

	def load_data(self):
		'''
		Loads data using the yahoo finance python api
		'''
		# Iterate over the name_list
		for i,name in enumerate(self.name_list):
			print '... Loading:', name, 'Index', i+1, 'of', len(self.name_list)
			# Call the yahoo finance API
			tmp_data = pd.DataFrame(
							yf.Share(name).get_historical(
										self.start_date.strftime('%Y-%m-%d'),
										self.end_date.strftime('%Y-%m-%d')))
			# Convert objects to numeric
			tmp_data = tmp_data.convert_objects(convert_numeric=True)	
			# Append the data
			self.data = self.data.append(tmp_data)
		# Convert date to date time object
		tmp_data['Date'] = tmp_data['Date'].astype('datetime64')
		# Set the index for easier data manipulation
		self.data = self.data.set_index(['Symbol', 'Date'])
		

	def enrich_data(self):
		'''
		Collection of function calls to enrich data
		'''
		# Enrich with within day uplift
		self.data['Within_Day'] = self.data.groupby(level='Symbol')\
							.apply(lambda x: within_day(x, rel=False)).values
		# Enrich with between day information
		self.data['Between_Day'] = self.data.groupby(level='Symbol')\
							.apply(lambda x: between_day(x, rel=False)).values
		# Enrich with within day uplift
		self.data['Within_Day_Rel'] = self.data.groupby(level='Symbol')\
							.apply(lambda x: within_day(x, rel=True)).values
		# Enrich with between day information
		self.data['Between_Day_Rel'] = self.data.groupby(level='Symbol')\
							.apply(lambda x: between_day(x, rel=True)).values


#===============================================================================
# Non class functions defining the enriching operations
#===============================================================================

def within_day(data, rel=False):
	'''
	Calculates the difference between opening an closing price.
	
	Args:
		data (pd.DataFrame: the financial data on which calculations are
			to be performed.
		rel (boolean): if set to false, the absolute difference is returned,
			else the relative difference is returned.
	
	Returns:
		pd.series of price difference using same index as data.
	'''
	# Apply the rel argument
	if rel:
		denominator = data['Open']
	else:
		denominator = 1.0
	# Create and return the series object
	return (data['Close'] - data['Open']) / denominator


def between_day(data, rel=True):
	'''
	Calculates the difference between opening price and closing price of the
	previous day.
	
	Args:
		data (pd.DataFrame: The financial data on which calculations are
			to be performed.
		rel (boolean): if set to false, the absolute difference is returned,
			else the relative difference is returned.
	
	Returns:
		pd.series of price difference using same index as data.
	'''
	# Apply the rel argument
	if rel:
		denominator = data['Close'].shift(-1)
	else:
		denominator = 1.0
	# Create and return the series object
	return (data['Open'] - data['Close'].shift(-1)) / denominator