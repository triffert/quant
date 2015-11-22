import pandas as pd

class Depot:
	'''
	'''
	def __init__(self, capital, fees, portfolio=None):
		# Copy parameters to class variables
		self.capital = capital
		self.fees = fees
		if portfolio is None:
			# Create empty portfolio
			self.portfolio = pd.DataFrame(columns=['Quantity', 'Price'])
		else:
			# Reference the parameter to the class variable
			self.portfolio = portfolio


	def buy(self, stock, price, quant=None):
		# Determine if capital is sufficient for quantity
		if quant is None or self.capital < quant * price:
			quant = int(self.capital / price)
		# Pay for stock and pay transaction fee
		self.capital -= quant * price + self.fees
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
									columns=['Price','Quantity'], index=[stock])
			self.portfolio = self.portfolio.append(new_stocks)


	def sell(self, stock, price, quant=None):
		# If stock is not owned do not do anything
		if stock not in self.portfolio.index:
			return
		# Determine if the asked number of stocks is owned
		if quant is None or quant > self.portfolio.loc[stock]['Quantity']:
			quant = self.portfolio.loc[stock]['Quantity']
		# Add money to capital and pay transaction fees
		self.capital += quant * price - self.fees
		# Remove stocks from portfolio
		self.portfolio.loc[stock]['Quantity'] -= quant
		# Delete row if all stocks were sold
		if self.portfolio.loc[stock]['Quantity'] <= 0:
			self.portfolio.drop(labels=stock, inplace=True)