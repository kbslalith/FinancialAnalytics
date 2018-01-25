import urllib.request
import numpy as np
import pandas as pd
from sklearn import linear_model,metrics
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import random
from datetime import datetime,timedelta
from sklearn.model_selection import train_test_split
import company_details as company_details
import design as design
import sys

val = []
indx = []
size = 0
i = 1

# This is to allow user to enter date in MM/DD/YYYY format
def enterdate():
    date = input("Enter the date for which you want prediction in MM/DD/YYYY format: ")
    return date

# This is used to predict the stock price
def prediction(regr,date_test,number):
    predict = regr.predict(number)
    return predict[0]

def timeGraph(cost,date,legend):
    cost = (cost[np.isfinite(cost)]) # this is where the shape changes
    val.append(cost.shape[0])
    cost = (np.array(cost.iloc[::-1])).reshape(cost.shape[0],1)
    date = (date.iloc[::-1])
    date = date[0:cost.shape[0]].values.reshape(cost.shape[0],1)
    plt.plot(date,cost,label = legend)
    plt.ylabel('Stock Price')
    plt.xlabel('Months')
    plt.legend(loc = 'best')
    plt.grid()
    return cost

# This function calculate the return of investment
def roi(regr,date_test,currentcost):
    design.design()
    investment = float(input("\nPlease Enter the Amount You want to invest: $"))
    shares = (investment/currentcost)
    investment_period = input("Enter till when you want to invest in the format MM/DD/YYYY :")
    value = datecal(investment_period)
    futureval = (prediction(regr,date_test,number=indx[0]+value))
    roi = (shares*futureval)
    print("\nCurrent Stock Price: $", currentcost)
    print("\nFuture Stock Price: $", futureval)
    print ("\nRoi is: $", roi)
    print ("\nProfit is: $", (roi-investment) )


# This is the menu function which allows user to select Check Cost Trend, Regression Graph, Prediction , Calculate returns from the entered date
def flow():
    design.design()
    data = pd.read_csv("file.csv", delimiter = ",",na_values=['-'])
    date = data['Date']
    date = pd.to_datetime(date)

    data['Date'] =  pd.to_datetime(data['Date'])
    data = data.sort_values(by=['Date'], ascending=[True])
    data.set_index('Date', inplace=True)
    data = data.resample('D').ffill().reset_index()

    data1 = data.drop_duplicates( subset= ['Volume','Open','Close'], inplace = True)
    date1 = data['Date']
    opencost = data['Open']
    closecost = data['Close']

    timeGraph(opencost,date1,legend = 'Open Cost Trend')
    timeGraph(closecost,date1, legend = 'Close Cost Trend')
    test = np.array(range(val[0]))

    test =  test.reshape(val[0],1)

    indx.append(data.index[-1])

    opencost = (opencost[np.isfinite(opencost)])
    opencost = opencost[0:val[0]]
    opencost_pr = opencost.values.reshape(val[0],1) # RESHAPPING TO SAME SHAPE

    global i
    global size
    if (i)==1:
        try:
            size = float(input("\nPlease enter Percentage of training size between (1 - 99): "))
        except:
            print ("\n Wrong Entry! Try again")
            flow()

        if size not in range(1,100):
            print("\nSorry Invalid Value please enter size between 0 to 100")
            flow()
        else:
            i += 1

    #TRAINING AND TESTING
    date_train, date_test, opencost_pr_train, opencost_pr_test = train_test_split(test,opencost_pr,random_state=1,train_size = (size)/100)

    regr = linear_model.LinearRegression()

    regr.fit(date_train, opencost_pr_train)

    answer = input("\n1. Check Cost Trend\n2. Regression Graph\n3. Predictor\n4. Calculate returns\n5. Go Back to previous menu\n6. Exit\n\n").upper()
    if answer=="1":
        plt.suptitle('Cost Trend')
        plt.show()

    elif answer=="2":
        plt.close()
        plt.scatter(test, opencost_pr,  color='green')
        plt.plot(date_test, regr.predict(date_test), color='blue', linewidth=3)
        plt.xlabel('Months')
        plt.ylabel('Stock Price')
        plt.suptitle('Linear Regression')
        plt.xticks(())
        plt.yticks(())
        plt.show()

    elif answer=="3":

        design.design()
        date = enterdate()
        try:
            no_of_days = datecal(date)
        except:
            print("\nSorry Wrong Input Try Again")
            flow()
        value = (indx[0] + no_of_days)
        predict = prediction(regr,date_test,number=value)
        prediction_Model = regr.predict(date_test)

        if predict < 0:
            print("\n\nCompany Not Listed At that time")

        else:
            print("\nPredicted value at %s for selected company is $%f" %(date,predict))
            # FOR R**2 value
            print ("\nR Squared Value is : ", metrics.r2_score(opencost_pr_test, prediction_Model))
            # Mean Square value
            print ("\nMean Squared error Value is : ", np.sqrt(((prediction_Model - opencost_pr_test) ** 2).mean()))

    elif answer == "4":
        try:
            roi(regr,date_test,closecost.iloc[-1])
        except:
            print("\n Oops Wrong Data Entry Retry")

    elif answer == "5":
        company_details.selectMenu()
    elif answer=="6":
        quitting()

    else:
        if input("Wrong Input! Press Any Key To Try Again or press 0 to exit: ")=="0":
            print ("\n************** THANK YOU **************")
            sys.exit()

    flow()

# This is used to select the size of the Training data
def trainsize():
    try:
        size = float(input("\nPlease enter Percentage of training size: "))
        print (size)
        trainsize.append(size)

    except:
        if input("\n Wrong Entry! Please retry or 0 to Exit") == "0":
            quitting()
        else:
            trainsize()

def quitting():
    print ("\n************** THANK YOU **************")
    sys.exit()

# This is used to calculate the days between the date entered and the current(today's) date
def datecal(date):
    date = pd.to_datetime(date)
    today_date = datetime.today().date()
    start_date = date.date()
    value = start_date - today_date
    return value.days
