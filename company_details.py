import urllib.request
import pandas as pd
import numpy as np
import sys
import os
import prediction_model as prediction
import design as design
import financial_indicators as financial_indicators

# Menu selection for financial indicators and prediction
def selectMenu() :
	design.design()
	value = input("1. Financial Details\n2. Prediction Model\n3. Exit\n\n")
	design.design()
	if value == "1":
		financial_indicators.main()
	elif value == "2":
		prediction.flow()
	elif value == "3" :
		print ("\n************** THANK YOU **************")
		sys.exit()
	else :
		print("Wrong Choice!!! Please retry")
		selectMenu()

def getMenuDetails():
	design.design()
	print("Please select from the below menu option :\n")
	value= input("1. More Details of the Company\n2. Exit\n\n")
	if value == "1" :
		selectMenu()
	elif value == "2" :
		print ("\n************** THANK YOU **************")
		sys.exit()
	else :
		print("Wrong Choice!!!! Please retry")
		getMenuDetails()

def containsAny(str, set):
    """Check whether 'str' contains ANY of the chars in 'set'"""
    return 1 in [i in str for i in set]

# This function is used to Download Company Details File
def getFile(company_symbol):
	print ("Company symbol is : ", company_symbol)
	if(containsAny(company_symbol,'~$^')):
		print("\nNo Information Available About This Company: Please retry")
	elif(company_symbol.count(".")>1):
		print("\nNo Information Available About This Company: Please retry")
	else:
		# It will download the company file from the link and save it to local directory
		#urllib.request.urlretrieve("https://www.google.com/finance/historical?output=csv&q="+company_symbol,"file.csv")
		# editted the URL for fetching data from google finance
		urllib.request.urlretrieve("http://finance.google.com/finance/historical?q={}&startdate=Nov+7%2C+2016&enddate=Nov+30%2C+2017&num=30&ei=NGoQWtDQFMGKUIuSsYgF&output=csv".format(company_symbol),"file.csv")
		getMenuDetails()


def main(x):
	getFile(x)
