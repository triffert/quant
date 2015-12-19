# Import external packages
import pandas as pd

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
				# Sell those stocks at current open pruce
				depot.sell(stock=stock, price=cur_open_price, quant=n_stocks)

