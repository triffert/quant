import pandas as pd

class Depot:
	'''
	'''
	def __init__(self, bankroll, fees, portfolio=None):
		# Copy parameters to class variables
		self.bankroll = bankroll
		self.fees = fees
		if portfolio is None:
			# Create empty portfolio
			self.portfolio = pd.DataFrame(columns=['Quantity', 'Price'])
		else:
			# Reference the parameter to the class variable
			self.portfolio = portfolio


	def buy(self, stock, quant=None, price):
		# Determine if bankroll is sufficient for quantity
		if quant is None or self.bankroll < quant * price:
			quant = int(self.bankroll / price)
		# Pay for stock
		self.bankroll -= quant * price
		# Add stock to portfolio
		if stock in self.portfolio.index:
			# Create temporary variables
			port_price = self.portfolio.loc[stock]['Price']
			port_quant = self.portfolio.loc[stock]['Quantity']
			# Update quantities and prices in portfolio
			self.portfolio.loc[stock]['Quantity'] = port_quant + quant
			self.portfolio.loc[stock]['Price'] = \
				(quant * price + port_quant * port_price) / (port_quant + quant)
		else:
			new_stocks = pd.DataFrame(data=[[price, quant]],
									columns=['Price','Quantity'], index=['AEG'])
			self.portfolio = self.portfolio.append(new_stocks)


	def sell(self, stock, quant=None, price):
		# If stock is not owned do not do anything
		if stock not in self.portfolio.index:
			return
		# Determine if the asked number of stocks is owned
		if quant is None or quant > self.portfolio.loc[stock]['Quantity']:
			quant = self.portfolio.loc[stock]['Quantity']
		# Add money to bankroll
		self.bankroll += quant * price
		# Remove stocks from portfolio
		self.portfolio.loc[stock]['Quantity'] -= quant