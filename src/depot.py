# External imports
import pandas as pd

#===============================================================================
# Class for depots 
#===============================================================================

class Depot:
	'''
	Class for easy depot management. Contains buying and selling functions.
	'''
	
	def __init__(self, capital, fees, portfolio=None):
		'''
		Constructor of the Depot class
		
		Args:
			capital (float): starting capital
			fees (float): transaction fees (applied to every buy and sell)
			portfolio (pd.DataFrame): specifies the owned stocks
		'''
		# Copy parameters to class variables
		self.capital = capital
		self.fees = fees
		# Set portfolio if not set
		if portfolio is None:
			# Create empty portfolio
			self.portfolio = pd.DataFrame(columns=['Quantity', 'Price'])
		else:
			# Reference the parameter to the class variable
			self.portfolio = portfolio


	def monetize(self, prices):
		'''
		Sell all stocks remaining in the portfolio for the specified price.
		
		Args:
			prices (pd.Series): Price per stock
		'''
		# If stocks are owned
		if not self.portfolio.empty:
			# Go through all of them
			for stock in self.portfolio.index.levels[0]:
				# Sell all
				self.sell(stock, prices.loc[stock])


	def buy(self, stock, price, quant=None):
		'''
		Purchases quant stocks at price and adds them to self.portfolio,
		while reducing self.capital by the due amount. Also self.fees are
		deducted from self.capital for this transaction.
		If capital is not sufficent for quant stocks, the maximum amount
		possible is purchased.
		
		Args:
			stock (string): identifier of the stock to purchase
			price (float): price at which a single stock can be purchased
			quant (integer): number of stocks to purchase. If set to None, then
				the maximum amount of stocks that can be purchased with the
				current self.capital balance is purchased.
		'''
		# Determine if capital is sufficient for quantity
		if quant is None or self.capital < quant * price + self.fees:
			quant = int( (self.capital - self.fees) / price)
		# If invalid quant value return
		if quant <= 0: return
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
			# Create row in self.portfolio by appending dataframe
			new_stocks = pd.DataFrame(data=[[price, quant]],
									columns=['Price','Quantity'], index=[stock])
			self.portfolio = self.portfolio.append(new_stocks)


	def sell(self, stock, price, quant=None):
		'''
		Sells quant stocks at price and removes them from self.portfolio,
		while adding the amount to self.capital. Also self.fees are
		deducted from self.capital for this transaction.
		If less than quant stocks are owned all are sold.
		
		Args:
			stock (string): identifier of the stock to sell
			price (float): price at which a single stock can be sold
			quant (integer): number of stocks to sell. If set to None, then
				the maximum amount of stocks that can be sold (as determined by
				the current portfolio) is sold.
		'''
		# If stock is not owned, do not do anything
		if stock not in self.portfolio.index: return
		# Determine if the asked number of stocks is owned
		if quant is None or quant > self.portfolio.loc[stock]['Quantity']:
			quant = self.portfolio.loc[stock]['Quantity']
		# If invalid quant value, do not do anything
		if quant <= 0: return
		# Calculate taxes (Abgeltungssteuer und Solidaritätszuschlag)
		taxes = max(0.0, 0.26375 * (price - (self.portfolio.loc[stock]['Price'])))
		# Add money to capital and pay transaction fees
		self.capital += quant * price - self.fees - taxes * quant
		# Remove stocks from portfolio
		self.portfolio.loc[stock]['Quantity'] -= quant
		# Delete row if all stocks were sold
		if self.portfolio.loc[stock]['Quantity'] <= 0:
			self.portfolio.drop(labels=stock, inplace=True)