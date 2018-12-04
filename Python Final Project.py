
# coding: utf-8

# In[ ]:


#Bradley Kyle Sturgis
#ISMN 5650
#Dr. Gupta
#Final Project
#Using BeautifulSoup to scrape for Amazon prices and compare them
#"Amazon Sleuth"


# In[ ]:


#TO DO LIST#
#Compare() function
#Automated Scheduled Scrapping
#Pretty Table of tracked items as part of display()
##(Optional) URL transformed as bit.ly link as part of table
#Visualization of scrapped data; time series line graph of prices
#Loop back to menu


# In[3]:


#Import BeautifulSoup and urllib and time
import bs4 as bs
import urllib.request
from time import localtime, strftime
import csv
import os


#Global variable price_IDS, which is a list of dictionaries that include identifiers for finding the price in the HTML of the Amazon page
price_IDS = [{"id": "priceblock_ourprice"},
             {"id": "priceblock_dealprice"},
             {"class": "a-size-medium a-color-price offer-price a-text-normal"},
            {"class": "a-size-base a-color-price offer-price a-text-normal"},
            {"id": "newBuyBoxPrice"},
            {"class": "a-size-mini twisterSwatchPrice"}]

#Other identifier not being used currently
#             {"class": "a-size-medium a-color-price"}


#Declare main() function
def main():
    
    sent = True
    reset = True
    #Present the user with a welccome message describing how the program works
    print("Hello. Welcome to Amazon Sleuth. Would you like add items to be tracked or check on items you have previously asked to be tracked?"+ "\n"+
         "Type ADD to add items to your tracking list or CHECK to check items that you have asked to be tracked \n"+
         "If this is your first time, type FIRST. If you want to exit, type EXIT.")
    #Allow user to enter command
    while sent:
      userCommand = str(input())
    
      #Determine what command was entered and run the appropriate function based on that
      if userCommand.upper() == 'FIRST':
          #Writes a new csv filled with info on the items the user provides via their Amazon URLs
          fileNew(addItems())
      elif userCommand.upper() == 'ADD':
      #Check for existance of master file
          if os.path.isfile('./AmazonItemsTest.csv') == True:
              fileAdd(addItems())
              print('File Add ran')
          else:
              print('Sorry, we do not have any previously tracked items on file; please enter in item URLs to start tracking: ')
              fileNew(addItems())
      elif userCommand.upper() == 'CHECK':
          displayCSV()
      if userCommand.upper() == 'EXIT':
          sent = False
          reset = False
          
      if reset:
        print("What do you want to do next? ")
    #Name of the master csv with the Amazon item data in it will be called 'AmazonItems.csv'
    
    #11/8/18 using 'AmazonItemsTest.csv' for testing purposes
    

    
    
def addItems():
        
    #Initialize an empty list for storing URLs of items that need to be tracked
    itemURLs = []
    #Prompt user for URL of the Amazon item they want to track
    while True:
        userInput = input("Please enter the URL of the Amazon item you would like to track: \n " +
                    "(Enter in 0 when you are finished entering in items)")
        if userInput == "0":
            print("Thank you for your input.")
            break
        itemURLs.append(userInput)
    #This will become a list of dictionaries with information on the Amazon items
    itemsInfo = []
    for url in itemURLs:
        #scrape_info function returns the name, price, and time as a dictionary with name as key and price and time as list value
        urlData = scrape_info(url)
        #Add the returned dictionary to a list
        itemsInfo.append(urlData)
    print(itemsInfo)
    return itemsInfo

def scrape_info(url):
    user_agent = "Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0"
    headers = {'User-Agent': user_agent}
    data = None
    req = urllib.request.Request(url, data, headers)
    sauce = urllib.request.urlopen(req).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')
    
    #Find the price on the Amazon page by checking for different tags that may contain the price
    #This function will loop through all known identifiers until it finds a price or runs out of identifiers to try
    for identifier in price_IDS:
        #Pass an identifier to the .find() function
        price_tag = soup.find("span", identifier)
        #If that identifier returned something, stop looking
        if price_tag != None:
            break
    
    #This block of code is in case there is no price on the page or the Amazon page is weird and the price is in a tag not known to us

    try:
        price = price_tag.text
    except:
        price = "Sorry, there is no available price for this item at this time"

    #Find the item name on the Amazon page
    itemName = soup.find("span", {"id": "productTitle"})
    
    amazonItem = {'Item': itemName.text.strip(), 'Price': price, 'Time': strftime("%Y-%m-%d %H:%M:%S", localtime()), 'URL': url }
    #amazonItem = { itemName.text.strip() : [price, strftime("%Y-%m-%d %H:%M:%S", localtime())]}
    return amazonItem

#Define function for fileNew(), which creates a new CSV and writes to it
def fileNew(newItems):
    with open('AmazonItemsTest.csv', 'w', newline='') as itemsFile: #11/8/18 using 'AmazonItemsTest.csv' for testing purposes
        fieldnames = ['Item', 'Price', 'Time', 'URL']
        theWriter = csv.DictWriter(itemsFile, fieldnames=fieldnames)
        
        theWriter.writeheader()
        for item in newItems:
            theWriter.writerow(item)
#Function for adding items to be tracked; similar to fileNew but items are appended to the end of the csv instead of
#Overwriting the csv entirely
def fileAdd(newItems):
    with open('AmazonItemsTest.csv', 'a', newLine='') as itemsFile: #11/8/18 using 'AmazonItemsTest.csv' for testing purposes
        fieldnames = ['Item', 'Price', 'Time', 'URL']
        theWriter = csv.DictWriter(itemsFile, fieldnames=fieldnames)
        
        for item in newItems:
#             print(item)
            theWriter.writerow(item)

#Define function for displaying items in the master csv file that stores the items and the prices
def displayCSV():
    with open('AmazonItemsTest.csv') as items:
        readCSV = csv.reader(items, delimiter=',')
        for row in readCSV:
            print(row)

# #Define function that finds the last UID, so that the scrapping function can ennumerate from that last UID when scrapping new items
# def lastUID():
#     UIDS = []
#     with open('AmazonItemsTest.csv') as csvfile:
#         readCSV = csv.reader(csvfile, delimiter=',')
        
#         for row in readCSV:
#             try:
#                 if row[4] == 'UID':
#                     pass
#                 else:
#                     UIDS.append(row[4])
#             except:
#                 continue
                
                
#             try:
#                 nextUID = max(UIDS)
#             except:
#                 print('exception')
#                 nextUID = 0
    
# #     print("nextUID: " + str(nextUID))
#     return nextUID



main()

