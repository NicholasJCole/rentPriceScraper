# program to scrape Dallas rent prices from rentjungle

import mechanize

import urllib2
import re
from BeautifulSoup import BeautifulSoup as bs
import csv

def get_html(starting_page):
    base_url = ['http://www.rentjungle.com/dallas-apartments-and-houses-for-rent/page:','/cla:32.802955/clo:-96.769923/']
    website_url = base_url[0] + str(starting_page) + base_url[1]
    br = mechanize.Browser()
    br.set_handle_robots(True)
    r = br.open(website_url)
    html = r.read()
    return html
    
    
html = get_html(5)


# get address info and sq feet, rent, and bed/bath info

# get this: <p class="apartmentAdd"> 2403 N Washington Ave, Dallas, TX 75204
#objects = re.findall(r'<p class="apartmentAdd"> (.*)', html)
#print objects # or just >>>objects


def get_data(html):
    # get data using bs
    soup = bs(html)
    apt_divs = soup.findAll('div', {"class" : "apartmentTable"})
    # iterate through divs and extract address and price/sq feet data
    # get divs called apartmentAdd ('p') and floorplanboxout ('div')
    # pattern to nix html
    p = re.compile(r'<.*?>')
    address_divs = []
    apt_details = []
    #get address and apt details
    for div in apt_divs:
        address_divs.append(p.sub('', str(div.findAll('p', {'class' : 'apartmentAdd'}))))
        #raw_table = div.findAll('div', {'class' : 'floorplanboxout'})
        # extract tables
        table = div.findAll("table")
        # remove commas so they don't cause problems with split(',') later
        table = re.sub(',', '', str(div.findAll("table")))
        table = p.sub(',', str(table)).split(',')
        #print p.sub('', str(div.findAll('p', {'class' : 'apartmentAdd'})))
        #print table
        apt_details.append(table)
    # clean details
    cleaned_details = []
    for num in range(0, len(apt_details)):
        temp_container = []
        for detail in apt_details[num]:
            if detail not in ('', '[', ']', 'Beds', 'Baths', 'Area (sq. feet)', 'Monthly Rent'):
                temp_container.append(detail)
        cleaned_details.append(temp_container)
    # clean address
    cleaned_addresses = []
    for i in address_divs:
        temp = re.sub(r'(-.+)', '', i)
        temp = re.sub(r'(\n)', '', temp)
        temp = re.sub(r'(\[ )', '', temp)
        cleaned_addresses.append(temp)
    for i in cleaned_details:
        print i
    return (cleaned_addresses, cleaned_details)

get_data(html)
# get tables
#html_tables = []
#soup = bs(html)
#tables = soup.findAll("table")
#for table in tables[:8]:
#    if table.findParent("table") is None:
#        html_tables.append(table)
    
# scrub data

#p = re.compile(r'<.*?>')
#cleaned_tables = []
#for line in p.sub(',', str(tables)).split(','):
#    if line not in ("", "[", "]"):
#        cleaned_tables.append(line)
        
#print cleaned_tables
#print len(cleaned_tables)
        






