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

# get address info and sq feet, rent, and bed/bath info

# change this into a function that returns all apartmentTables
# and then create two different functions for getting 
# details and address
def get_tables(html):
    'gets apartmentTable divs from rentjungle'
    soup = bs(html)
    apt_tables = soup.findAll('div', {"class" : "apartmentTable"})
    return apt_tables

def get_zip_codes(apt_tables):
    'takes input of apt tables and outputs zip codes'
    # do I want to get full addresses or just zip codes?
    # really only need zip codes
    zip_codes = []
    for table in apt_tables:
        zip_code = str(table.findAll('p', {'class' : 'apartmentAdd'}))
        #re.findall(pattern, string, flags=0)
        zip_code = re.findall(r'TX \d{5}', address)
        zip_codes.append(zip_code)
    return zip_codes
    
def get_apt_details(apt_tables):
    'takes input of apt tables and outputs details'
    apt_details = []
    p = re.compile(r'<.*?>')
    # extract data
    # instead, go to link with full table of details, extract this
    for table in apt_tables:
        raw_details = table.findAll("table")
        # get rid of commas so we can split data via commas later
        raw_details = re.sub(r',', '', str(raw_details))
        raw_details = p.sub(',', raw_details)
        apt_details.append(raw_details.split(','))
    # clean the data, get rid of non numbers
    return apt_details
    
    

def write_csv(data):
    with open('data_file.csv', 'wb') as csvfile:
        datawriter = csv.writer(csvfile, delimiter = ',',)
        for i in data:
            datawriter.writerow(i)


def main():
    html = get_html(5)
    apt_tables = get_tables(html)
    tables = get_tables(html)
    return tables
    
data = main()

print data

