#import pandas as pd
#import simulator as ss

def strategy_nothing(bank, data, portfolio, time, stocks, fees):
	# Do not buy stocks - Baseline for all comparisons
	return bank

def strategy_inter_day_even(bank, data, portfolio, time, stocks, fees):
	'''
	Buy at end of previous day sell at opening of current day.
	Uniformly distribute money for all stocks
	'''
	# Calculate amount of money available per purchase
	bank_per_stock = bank / len(stocks) - fees
	# Initialization of output variable
	new_bank = bank
	# Purchase of stocks and monetization
	for stock in stocks:
		if time in data.loc[stock].index \
			and bank_per_stock >= data.loc[stock,time]['Prev_Close']:
			# Determine number of stocks that can be bought
			n_stocks = int(bank_per_stock / data.loc[stock,time]['Prev_Close'])
			# Buy previous day stocks and then sell them at opening price
			new_bank -= n_stocks * data.loc[stock,time]['Prev_Close'] + fees
			new_bank += n_stocks * data.loc[stock,time]['Open']
		else:
			new_bank += bank_per_stock + fees
	# Return the new bank roll
	return new_bank

def strategy_inter_day_even_hold_if_less(bank, data, portfolio, time, stocks, fees):
	'''
	Buy at end of previous day sell at opening of current day.
	As long as open price dropped compared to closing price keep them.
	Uniformly distribute money for all stocks.
	'''
	# Calculate amount of money available per purchase
	bank_per_stock = bank / len(stocks) - fees
	# Initialization of output variable
	new_bank = bank
	# Purchase of stocks and monetization
	for stock in stocks:
		if time in data.loc[stock].index \
			and bank_per_stock >= data.loc[stock,time]['Prev_Close']:
			# Determine number of stocks that can be bought
			n_stocks = int(bank_per_stock / data.loc[stock,time]['Prev_Close'])
			new_bank -= fees + n_stocks * data.loc[stock,time]['Prev_Close']
			# Portfolio at purchase
			new_bank -= n_stocks * data.loc[stock,time]['Prev_Close'] + fees
			print portfolio.loc[stock]['n_stock']
			portfolio.loc[stock]['n_stock'] += n_stocks 
			print portfolio.loc[stock]['n_stock']
			# Buy previous day stocks and then sell them at opening price
			if data.loc[stock,time]['Open'] > data.loc[stock,time]['Prev_Close']:
				new_bank += portfolio.loc[stock]['n_stock']\
							 * data.loc[stock,time]['Open']
		else:
			new_bank += bank_per_stock + fees
	# Return the new bank roll
	return new_bank

def strategy_inter_kelley_crit_cov(bank, data, portfolio, time, stocks, fees):
	'''
	Buy at end of previous day sell at opening of current day.
	Distribute according to kelley criterion based on mean of previous sales
	'''
	pass