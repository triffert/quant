################################################################################
# A small script for playing around with the Yahoo-finance API
################################################################################

import yahoo_finance as yf
import pandas as pd

# TODO: Split into seperate modules

# Fees per trade in bank roll units
FEES = 1
START = pd.to_datetime('2013-11-01')
END = pd.to_datetime('2014-11-01')

# All companies in the DAX
DAX = ['ADS.DE','ALV.DE','BAS.DE','BAYN.DE','BEI.DE','BMW.DE','CBK.DE',
		'CON.DE','DAI.DE','DB1.DE','DBK.DE','DPW.DE','DTE.DE','EOAN.DE',
		'FME.DE','FRE.DE','HEI.DE','HEN3.DE','IFX.DE','LHA.DE','LIN.DE',
		'LXS.DE','MRK.DE','MUV2.DE','RWE.DE','SAP.DE','SDF.DE','SIE.DE',
		'TKA.DE','VOW3.DE']

class FinanceData:
	'''
	Class containing financial data, loading, cleaning and enriching functions 
	'''
		
	def __init__(self, name_list, start_date=START,
				end_date=END):
		'''
		Constructor
		'''
		# Copy the parameters to class variables
		self.name_list = name_list
		self.start_date = start_date
		self.end_date = end_date
		# Load the data
		self.load_data()
		# Enrich the data
		self.enrich_data()
		

	def load_data(self):
		'''
		Loads data as specified by class variables
		'''
		print 'Loading data'
		self.data = pd.DataFrame()
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
		# Enrich with previous closing date for convenience
		self.data['Prev_Close'] = self.data.groupby(level='Symbol')\
											.apply(prev_close).values
		# Enrich with within day uplift
		self.data['Within_Day'] = self.data.groupby(level='Symbol')\
											.apply(intra_day).values
		# Enrich with between day information
		self.data['Between_Day'] = self.data.groupby(level='Symbol')\
											.apply(inter_day).values
		# Enrich with within day uplift
		self.data['Within_Day_Rel'] = self.data.groupby(level='Symbol')\
											.apply(intra_day_rel).values
		# Enrich with between day information
		self.data['Between_Day_Rel'] = self.data.groupby(level='Symbol')\
											.apply(inter_day_rel).values

# Non class functions for enriching
def prev_close(data):
	return data['Close'].shift(-1)

def intra_day(data):
	return data['Close'] - data['Open']

def inter_day(data):
	return data['Open'] - data['Close'].shift(-1)
	
def intra_day_rel(data):
	return (data['Close'] - data['Open'])/abs(data['Open'])

def inter_day_rel(data):
	return (data['Open'] - data['Close'].shift(-1))/abs(data['Close'].shift(-1))