
import requests
from bs4 import BeautifulSoup
import numpy as np

# define a symbol to search
stock_symbol = "ARKQ"

# base url
base = "https://finance.yahoo.com"

# url to particular stock
endpoint = base + "/quote/{}".format(stock_symbol)

# request it & parse it
response = requests.get(endpoint).content
soup = BeautifulSoup(response, 'html.parser')

# these two sections contain the information for the summary page, so grab them to be parsed later.
left_summary_table = soup.find_all('div', {'data-test':'left-summary-table'})
right_summary_table = soup.find_all('div', {'data-test':'right-summary-table'})

# find the nav menu to get the other page links
nav_menu = soup.find('div', {'id':'quote-nav'})

# store the links in a dictionary
link_dictionary = {}

for anchor in nav_menu.find_all('a'):
    
    # grab the text (Page Name), link to page, and store the full link in the dictionary.
    text = anchor.text
    full_link = base + anchor['href']        
    link_dictionary[text] = full_link

#print ra cái link list
print(link_dictionary)

# build our split list function
def split_list(my_list, chunks):    
    return [my_list[i:i + chunks] for i in range(0, len(my_list), chunks)]

# SECTION ONE - PARSE THE SUMMARY PAGE

# grab the `tbody` for both the left and right side.
tbody_left = left_summary_table[0].tbody
tbody_right = right_summary_table[0].tbody

# define a list to store both tables
major_list = []

# append the parsed table to the master list.
major_list.append([item.text for item in tbody_left.find_all('td')])
major_list.append([item.text for item in tbody_right.find_all('td')])

# create a chunked version of our master list.
summary_data = [chunk for item in major_list for chunk in split_list(item, 2)]
summary_data

# make it number friendly
for row in summary_data:

    # handle the precentage case
    if '%' in row[1]:        
        row[1] = float(row[1].replace('%',''))/100
    
    # handle the split case X
    elif 'x' in row[1]:
        row[1] = row[1].split(' x ')
    
    # handle the split case -
    elif '-' in row[1]:
        row[1] = row[1].split(' - ')
    
    # handle the ,
    elif ',' in row[1]:
        row[1] = float(row[1].replace(',',''))
     
    # handle missing values
    elif 'N/A' in row[1]:
        row[1] = np.nan
        
#print ra ngó thử
print(summary_data)

#SECTION TWO - PARSE THE HOLDING PAGE

# define the link to the page
link = link_dictionary['Holdings']

# request the link and dump the content into the parser.
response = requests.get(link)
soup = BeautifulSoup(response.content, 'html.parser')

# We have to define a list of items we don't want. Luckily there are only a few items we need to avoid.
skip_list = ['',stock_symbol,'Sector','Average']

# find all the span elements labeled with start and end.
items = soup.find_all('span', {'class':['Fl(start)','Fl(end)']})

# loop through the parsed content, grab the text, and make sure it's not in the skip_list.
unsplit_data = [item.text for item in items if item.text not in skip_list ]

# split the list into chunks
holdings_data = [chunk for chunk in split_list(unsplit_data, 2)]  

# make number friendly
for row in holdings_data:
    
    if '%' in row[1]:        
        row[1] = float(row[1].replace('%',''))/100
        
    elif 'N/A' in row[1]:
        row[1] = np.nan
        
print(holdings_data)
