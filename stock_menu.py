'''

Front End Menu Code

Bhaskar Kuchimanchi (17200052)
Harshit Jain (17200167)
Meenal Rewatkar (17200165)

'''
import sys
import numpy as np
import pandas as pd
import company_details as company_details
import design as design
import webbrowser
import warnings
import re

warnings.simplefilter(action='ignore', category=FutureWarning) # Dont show User Pandas Warnings
warnings.simplefilter(action='ignore', category=UserWarning) # Dont show User Pandas Warnings
companylist = pd.read_csv('companylist.csv', delimiter = ",")
companynames = companylist['Name']
# Header Names : Symbol,Name,LastSale,MarketCap,IPOyear,Sector,industry,Summary Quote

print ("\n****Welcome To FinInfo Analytics****\n\t  Select an option")

def mainmenu():
    val = input("1. Enter Company Name\n2. Enter Company Symbol\n3. List of Symbols\n4. Exit\n\n") # Exit option can be included
    getdetails(val)
    return

# This is used to allow user to enter company name or symbol to view its details
def getdetails(x):
    if x == "1":
        name = input("Please enter: ")
        for i in companynames:
        	if (re.search(name, i , re.IGNORECASE)) is not None:
        		getinfo(i)
    elif x == "2":
        symbol = input("Please enter Symbol: ").upper()
        getinfo(symbol)
    elif x == "3":
        print (companylist["Symbol"],"\n\n")
        mainmenu()
    elif x == "4":
        print ("\n************** THANK YOU **************")
        sys.exit()
    else :
        print ("Please retry\n")
    print("\nPlease Enter Properly\n")
    mainmenu()

# This function is used to fetch each company's details from companydetails.csv
def getinfo(x):
    companies = (companylist[(companylist == x).any(1)].stack())

    if len(companies) == 0: # HANDLING ERROR
        print ("Company Not Found :   *Please enter exact name or symbol* \n")
        value = input("If you want to try more please enter Y or enter N to go back to previous menu: ")
        if value.upper() == "Y":
            getdetails("2")
        elif value.upper() == "N":
            design.design()
            mainmenu()
        else:
            print("\nWrong Choice !!!!!! Please retry")
            getdetails("2")

    elif len(companies)>8:
        print ("\n Oops it does'nt look like a correct symbol - Looking For Anyone of these?")
        design.design()
        print(companies[0:],"\n")
        design.design()
        if input("\nif not in the list? Hit 0 to try again OR any key to continue: ") == "0":
            main()
        else :
            np
        confirm = input("confirm the Company Symbol by entering : ").upper() #Upper to handle case sensitive execpts
        design.design()
        try:
            x = (np.where(companylist.Symbol == confirm))
            p = int(x[0])
            print (companylist.iloc[p][0:7])
            val = input("To visit company's Nasdaq site press Y or to continue press any other key: ")
            if(val.upper() == "Y"):
                webbrowser.open(companylist[7]) # To open the company link for more info
            company_details.getFile(confirm)
            main()
        except:
            print("\nInvalid Entry Try Again")
            getdetails("2")

    else:
        design.design()
        print((companies[0:7]),"\n") #For memory quote in companies[8]
        val = input("To visit company's Nasdaq site press Y or to continue press any other key: ").upper()
        if(val == "Y"):
            print("opening url")
            webbrowser.open(companies[7]) # To open the company link for more info
        pih = 'PIH'
        if(x == pih):
            company_details.main(x)
        else:
            company_details.main(companies[0])
        design.design()

def main():
    mainmenu()

main()
