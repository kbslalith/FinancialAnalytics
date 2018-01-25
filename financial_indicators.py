import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import design as design
import dateutil.relativedelta
import company_details as company_details

# This function reads The downloaded company CSV file
def getCompanyData():
	df = pd.read_csv("file.csv") # Read CSV file
	df.head()
	df['Date'] = pd.to_datetime(df['Date'])
	new_date = df['Date'].dt.date
	start_date = new_date[0]
	return df,start_date

# This function is used to calculate weighted moving average and macd
def calculate(closecost):
	nslow=26
	nfast=12
	emaslow = pd.ewma(closecost, span=nslow, min_periods=1)
	emafast = pd.ewma(closecost, span=nfast, min_periods=1)
	MACD = emafast-emaslow
	result = pd.DataFrame({'MACD': MACD,'emaSlw': emaslow,'emaFst': emafast})
	return result

# This function is used to plot the graph of Exponential Weighted Moving Average
def weighted_moving_average(closecost):
	
	result = calculate(closecost)
	emaslow = result['emaSlw']
	emafast = result['emaFst']

	ax = emaslow.plot(label='emaslow')
	emafast.plot(ax=ax,label ='emafast')
	closecost.plot(ax=ax,label='cost trend')
	plt.legend(loc = 'best')
	plt.xlabel('Days')
	plt.ylabel('Stock Price')
	plt.suptitle('Weighted Moving Average')
	plt.show()

# This is used to show the graph of MACD
def macd(closecost):
	result = calculate(closecost)
	MACD = result['MACD']
	MACD.plot()
	plt.xlabel('Days')
	plt.ylabel('MACD Values')
	plt.suptitle('MACD')
	plt.show()

# This is used to calculate and plot the graph of moving average by passing Close Cost of the company
def moving_average(closecost):
	design.design()
	try:
		n = int(input("\nEnter the value of n for calculating moving average: "))
	except:
		print("\nWrong Entry Please Try Again")
		otherFinancialDetails()

	value = pd.rolling_mean(closecost,n)
	ax = value.plot()
	plt.xlabel('Days')
	plt.ylabel('Stock Price')
	plt.suptitle('Moving Average')
	plt.show()

# This is used to calucle Coefficient of varriation by using Close cost of the company
def cv(closecost):
	mean_close = closecost.mean()
	std_close = closecost.std()
	cv = float(std_close / mean_close)
	print("\nCoefficient of Variation :",cv)

# This function shows the menu options of moving average, weighted moving average, macd and coefficient of variation
def otherFinancialDetails():
	design.design()
	df,start_date = getCompanyData()

	df = df.sort_values(by=['Date'], ascending=[True])
	df.set_index('Date', inplace=True)
	df = df.resample('D').ffill().reset_index()

	closecost = df['Close']
	opencost = df['Open']
	value = input("\n1. Moving Average\n2. Weighted Moving average\n3. MACD(Moving Average Conversion Diversion)\n4. Coefficient of Variation\n5. Go Back To previous Menu\n6. Exit\n\n")
	if(value == "1"):
		moving_average(closecost)
	elif(value == "2"):
		weighted_moving_average(closecost)
	elif(value == "3"):
		macd(closecost)
	elif(value == "4"):
		cv(closecost)
	elif(value == "5"):
		financeMenu()
	elif(value == "6"):
		print ("\n************** THANK YOU **************")
		sys.exit()
	else :
		print("\nWrong Choice !!! Please retry")
		otherFinancialDetails()

	otherFinancialDetails()

# This function is used to print the basic financial details which includes mean,
# variance, standard deviation, quartiles etc
def basicFinancialDetails():
	design.design()
	value = input("\n1. Last 1 Year\n2. Last 6 Months\n3. Last 3 Months\n4. Go back to previous menu\n5. Exit\n\n")
	design.design()
	df, start_date= getCompanyData()
	if value == "1":
		end_date = start_date - dateutil.relativedelta.relativedelta(months=12)

	elif value == "2":
		end_date = start_date - dateutil.relativedelta.relativedelta(months=6)

	elif value == "3":
		end_date = start_date - dateutil.relativedelta.relativedelta(months=3)

	elif value == "4":
		financeMenu()

	elif value == "5":
		print ("\n************** THANK YOU **************")
		sys.exit()
	else :
		print("\nWrong Choice !!! Please retry")
		basicFinancialDetails()

	if value == "1" or value =="2" or value == "3":
		print("Trading at ",df['Open'][1],"as of ",df['Date'][1])
		design.design()
		mask=(df['Date']> end_date ) & (df['Date'] < start_date)
		df = df.loc[mask]
		financialDetails= df.describe()
		print(financialDetails)

	basicFinancialDetails()

# This function gives the menu option to select the basic or detailed financial details
def financeMenu():
	plt.clf()      # To close all the opened graphs from memory
	design.design()
	print("\nPlease select from the below options to see finance details : \n")
	value = input("1. Basic Financial Details\n2. Other Financial Details \n3. Go back to previous menu\n4. Exit\n\n")
	if(value == "1"):
		basicFinancialDetails()
	elif(value == "2"):
		otherFinancialDetails()
	elif(value == "3"):
		company_details.selectMenu()
	elif(value == "4"):
		print ("\n************** THANK YOU **************")
		sys.exit()
	else :
		print("\nWrong Choice!!! Please retry")
		financeMenu()

def main():
	financeMenu()
