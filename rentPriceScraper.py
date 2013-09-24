# program to scrape Dallas rent prices from rentjungle

import mechanize
import urllib2
import re
from BeautifulSoup import BeautifulSoup as bs
import csv

def get_html(website_url):
    website_url = 'http://www.rentjungle.com/dallas-apartments-and-houses-for-rent/page:6/cla:32.802955/clo:-96.769923/'
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
        zip_code = re.findall(r'TX \d{5}', zip_code)
        zip_codes.append(zip_code)
    return zip_codes
    
def get_apt_details(apt_tables):
    'takes input of apt tables and outputs details'
    apt_details = []
    p = re.compile(r'<.*?>')
    # extract data
    # instead, go to link with full table of details, extract this
    for table in apt_tables:
        # get link to table page
        if re.findall(r'(/apartments/ajax_floorplans/\w*/\w*)', str(table))[0]:
            full_details_link = 'http://www.rentjungle.com/' + re.findall(r'(/apartments/ajax_floorplans/\w*/\w*)', str(table))[0]
            full_details = get_full_details_table(full_details_link)
        else:
            full_details_link = "NA"
    # need to order the data
    return full_details
    
    
def get_full_details_table(full_details_link):
    'gets tables from detailed table page'
    p = re.compile(r'<.*?>')
    html = get_html(full_details_link)
    soup = bs(html)
    raw_details_tables = soup.findAll('table', {"class" : "fpBox"})
    # get rid of commas in dollar values
    raw_details_tables = re.sub(r',', '', str(raw_details_tables))
    # get rid of dollar signs and spaces
    raw_details_tables = re.sub(r'\$ ', '', str(raw_details_tables))
    raw_details_tables = p.sub(',', raw_details_tables)
    # clean tables
    raw_details_tables = raw_details_tables.split(',')
    # get rid of empties and brackets
    full_details_tables = []
    for detail in raw_details_tables:
        if detail not in ('Beds', 'Baths', 'Area (sq. feet)', 'Monthly Rent', '', ' ', '[', ']'):
            full_details_tables.append(detail)
    return full_details_tables
    
    

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

