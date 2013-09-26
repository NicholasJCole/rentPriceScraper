# program to scrape Dallas rent prices from rentjungle

import mechanize
import urllib2
import re
from BeautifulSoup import BeautifulSoup as bs
import csv
import time

#'http://www.rentjungle.com/dallas-apartments-and-houses-for-rent/page:6/cla:32.802955/clo:-96.769923/'

def get_html(website_url):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    # add some error handling here
    # perhaps make function retry if taking too long
    # urllib2.URLError: <urlopen error [Errno -2] Name or service not known>
    try:
        r = br.open(website_url)
        html = r.read()
    except urllib2.URLError as e:
        html = e.reason
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
    p = re.compile(r'<.*?>')
    full_details = []
    structured_details = []
    # extract data
    # instead, go to link with full table of details, extract this
    for table in apt_tables:
        # get link to table page
        full_details_link_base = re.findall(r'(/apartments/ajax_floorplans/\w*/\w*)', str(table))[0]
        if full_details_link_base:
            full_details_link = 'http://www.rentjungle.com/' + full_details_link_base
            full_details.append(get_full_details_table(full_details_link))
            time.sleep(1)
        else:
            full_details.append("NA")
    for detail_piece in full_details
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
        if detail not in ('Beds', 'Baths', 'Area (sq. feet)', 'Monthly Rent', '', ' ', '[', ']', '\n'):
            full_details_tables.append(detail)
    # need to arrange details
    return full_details_tables
    
# add a scrub data function to combine
# both zips and details/arrange details in a logical format

def write_csv(data):
    with open('data_file.csv', 'wb') as csvfile:
        datawriter = csv.writer(csvfile, delimiter = ',',)
        for i in data:
            datawriter.writerow(i)


def main():
    html = get_html('http://www.rentjungle.com/dallas-apartments-and-houses-for-rent/page:6/cla:32.802955/clo:-96.769923/')
    apt_tables = get_tables(html)
    full_details = get_apt_details(apt_tables)
    zip_codes = get_zip_codes(apt_tables)
    return (full_details, zip_codes)
    
#data = main()

#print data

