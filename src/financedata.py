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

DAX = pd.np.random.permutation(DAX)

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
		self.start_date = pd.to_datetime(start_date)
		self.end_date = pd.to_datetime(end_date)
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
			print('... Loading:', name, 'Index', i+1, 'of', len(self.name_list))
			# Call the yahoo finance API
			tmp_data = pd.DataFrame(
							yf.Share(name).get_historical(
										self.start_date.strftime('%Y-%m-%d'),
										self.end_date.strftime('%Y-%m-%d')))
			# Convert objects to numeric
			tmp_data = tmp_data.apply(pd.to_numeric, args=('ignore',))
			# Append the data
			self.data = self.data.append(tmp_data)
		# Convert date to date time object
		tmp_data['Date'] = tmp_data['Date'].astype('datetime64')
		# Set the index for easier data manipulation
		self.data = self.data.set_index(['Symbol', 'Date'])
		

	def enrich_data(self):
		'''
		Collection of function calls to enrich data
		
		Reshape is necessary for 1 level case due to groupby bug explained here:
			https://github.com/pydata/pandas/issues/5839
		'''
		# Enrich with within day uplift
		self.data['Within_Day'] = pd.np.reshape(
				self.data.groupby(level='Symbol')\
				.apply(lambda x: within_day(data=x, rel=False)).values,
				(len(self.data,)))
		# Enrich with between day information
		self.data['Between_Day'] = pd.np.reshape( 
				self.data.groupby(level='Symbol')\
				.apply(lambda x: between_day(data=x, rel=False)).values,
				(len(self.data,)))
				# Enrich with between day information
		self.data['Previous_Day_1'] = pd.np.reshape( 
				self.data.groupby(level='Symbol')\
				.apply(lambda x: previous_day(data=x, rel=False, i=1)).values,
				(len(self.data,)))
		# Enrich with between day information
		self.data['Previous_Day_2'] = pd.np.reshape( 
				self.data.groupby(level='Symbol')\
				.apply(lambda x: previous_day(data=x, rel=False, i=2)).values,
				(len(self.data,)))
		# Enrich with between day information
		self.data['Previous_Day_3'] = pd.np.reshape( 
				self.data.groupby(level='Symbol')\
				.apply(lambda x: previous_day(data=x, rel=False, i=3)).values,
				(len(self.data,)))
		# Enrich with within day uplift
		self.data['Within_Day_Rel'] = pd.np.reshape(
				self.data.groupby(level='Symbol')\
				.apply(lambda x: within_day(data=x, rel=True)).values,
				(len(self.data,)))
		# Enrich with between day information
		self.data['Between_Day_Rel'] = pd.np.reshape( 
				self.data.groupby(level='Symbol')\
				.apply(lambda x: between_day(data=x, rel=True)).values,
				(len(self.data,)))
		# Enrich with between day information
		self.data['Previous_Day_Rel_1'] = pd.np.reshape( 
				self.data.groupby(level='Symbol')\
				.apply(lambda x: previous_day(data=x, rel=True, i=1)).values,
				(len(self.data,)))
		# Enrich with between day information
		self.data['Previous_Day_Rel_2'] = pd.np.reshape( 
				self.data.groupby(level='Symbol')\
				.apply(lambda x: previous_day(data=x, rel=True, i=2)).values,
				(len(self.data,)))
		# Enrich with between day information
		self.data['Previous_Day_Rel_3'] = pd.np.reshape( 
				self.data.groupby(level='Symbol')\
				.apply(lambda x: previous_day(data=x, rel=True, i=3)).values,
				(len(self.data,)))
		

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
		denominator = data['Close']
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
		denominator = data['Close']
	else:
		denominator = 1.0
	# Create and return the series object
	return (data['Open'].shift(1) - data['Close']) / denominator


def previous_day(data, rel=True, i=1):
	'''
	Calculates the difference between opening price and closing price of the
	previous day (i days in the past).
	
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
		denominator = data['Close']
	else:
		denominator = 1.0
	# Create and return the series object
	return ((data['Open'].shift(1) - data['Close']) / denominator).shift(-i)