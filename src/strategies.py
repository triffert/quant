# Import external packages
import pandas as pd
import random as rd

#===============================================================================
# Module containing strategies
#===============================================================================

def no_trade(data, depot, time, **kwargs):
	'''
	Basic non-strategy. Only for testing purposes.

	Args:
		data (pd.DataFrame: the financial data on which calculations are
			to be performed.
		depot (Depot object): depot for the strategy 
		time (pd.timestep): point in time the strategy is applied
	'''
	# Do not do anything - Baseline for trivial comparisons
	pass


def inter_day_even(data, depot, time, **kwargs):
	'''
	Buy at closing price of previous day sell at opening of current day. 
	Uniformly distribute money for all stocks.
	
	Args:
		data (pd.DataFrame: the financial data on which calculations are
			to be performed.
		depot (Depot object): depot for the strategy 
		time (pd.timestep): point in time the strategy is applied
	'''
	# Get list of available stocks
	available = data.index.levels[0]
	# Calculate amount of money available per purchase
	bank_per_stock = depot.capital / len(available) - depot.fees
	# Purchase of stocks and monetization
	for stock in available:
		if time in data.loc[stock].index:
			# Get previous day closing price
			prev_close_price = data.loc[stock].shift(-1).loc[time]['Close']
			# Only if the previous data exists purchase
			if not pd.np.isnan(prev_close_price):
				# Determine number of stocks that can be bought.
				n_stocks = max(int(bank_per_stock / prev_close_price), 0)
				# Buy n_stocks at previous day closing price
				depot.buy(stock=stock, price=prev_close_price, quant=n_stocks)
				# Current opening price
				cur_open_price = data.loc[stock,time]['Open']
				# Sell those stocks at current open price
				depot.sell(stock=stock, price=cur_open_price, quant=n_stocks)


def inter_day_greedy(data, depot, time, **kwargs):
	'''
	Buy at closing price of previous day sell at opening of current day. 
	Invest all money into the stock which had best inter day performance in the
	past, based on counts of how often it was positive in relation to number of
	days traded.
	
	Args:
		data (pd.DataFrame: the financial data on which calculations are
			to be performed.
		depot (Depot object): depot for the strategy 
		time (pd.timestep): point in time the strategy is applied
		kwargs: include t_len (in trading days)

	ATTENTION: THIS FUNCTION IS ONLY A ROUGH APPROXIMATION
		* NO CHECK IF THE STOCK WAS AVAILABLE AT TIME
		* NEEDS TO BE TESTED FOR CORRECTNESS 
	'''	
	# Get list of available stocks
	available = data.index.levels[0]
	# Count number of times a stock had positive interday performance
	p_inter = pd.DataFrame(index=available)
	# Define counting/frequency function
	def p_pos(x, t_len, field='Previous_Day_1'):
		return sum([y > 0 for y in x.iloc[0:t_len][field]])/float(t_len)
	# Apply counting to given data
	p_inter['p_pos'] =  data.groupby(level='Symbol')\
				.apply(lambda x: p_pos(x, kwargs['t_len'])).values
	# Chose stock based on passed data
	chosen_stock = p_inter.idxmax()[0]
	# Ensure stock is traded on given date
	if time in data.loc[chosen_stock].index:
		# Get previous day closing price
		prev_close_price = data.loc[chosen_stock].shift(-1).loc[time]['Close']
		# Only if the previous data exists purchase
		if not pd.np.isnan(prev_close_price):
			# Buy n_stocks at previous day closing price
			depot.buy(stock=chosen_stock, price=prev_close_price)
			# Current opening price
			cur_open_price = data.loc[chosen_stock,time]['Open']
			# Sell those stocks at current open price
			depot.sell(stock=chosen_stock, price=cur_open_price)
	# Only for some data exploration purposes
	return p_inter


def inter_day_random(data, depot, time, **kwargs):
	'''
	Buy at closing price of previous day sell at opening of current day. 
	Invest all money into a random stock.
	
	Args:
		data (pd.DataFrame: the financial data on which calculations are
			to be performed.
		depot (Depot object): depot for the strategy 
		time (pd.timestep): point in time the strategy is applied
	'''	
	# Get list of available stocks
	available = data.index.levels[0]
	# Chose stock based on passed data
	chosen_stock = rd.choice(available)
	# Ensure stock is traded on given date
	if time in data.loc[chosen_stock].index:
		# Get previous day closing price
		prev_close_price = data.loc[chosen_stock].shift(-1).loc[time]['Close']
		# Only if the previous data exists purchase
		if not pd.np.isnan(prev_close_price):
			# Buy n_stocks at previous day closing price
			depot.buy(stock=chosen_stock, price=prev_close_price)
			# Current opening price
			cur_open_price = data.loc[chosen_stock,time]['Open']
			# Sell those stocks at current open price
			depot.sell(stock=chosen_stock, price=cur_open_price)