#!/usr/bin/env python3

"""
Script to scrape dive bar data from Yelp

To do:
    - generalize to any city
    - program to rank bars by dive depth
    - output from sqlite db to webpage via Django
"""


#imports
from simpleget import *
from bs4 import BeautifulSoup
from collections import namedtuple
import sql_funcs



#constants
BASE_URL = 'https://www.yelp.com'
URL_PARAMS = '/search?cflt=divebars&find_desc=bars&find_loc=boise%2C%20idaho'
GET_URL = BASE_URL + URL_PARAMS
SQL_FILE = 'divebar_db.sqlite'


#namedtuple defs
DiveBarTup = namedtuple('DiveBarTup', [
    'name',
    'address',
    'rank',
    'url' ])



def extract_data(raw_html):
    """
    Uses BeautifulSoup and lxml to parse data from Yelp 
    Assumes Yelp filter for "dive bar" tag in a particular city
    """

    css_class_1 = 'lemon--div__373c0__1mboc largerScrollablePhotos__373c0__3FEIJ'
    css_class_2 = ' arrange__373c0__UHqhV border-color--default__373c0__2oFDT'
    css_class = css_class_1 + css_class_2

    parsed = BeautifulSoup(raw_html, features='lxml')

    bar_list = []

    for div in parsed.find_all('div', class_=css_class):
        anchor = div.find('a')
        url = anchor.get('href')
        if url[:4] != '/biz':   #ignore urls that aren't for businesses
            continue
        url = BASE_URL + url
        name = anchor.text.strip()
        rank = 1
        address_element = div.find('address')
        address = address_element.div.span.text.strip()

        bar_list.append(DiveBarTup(name, address, rank, url))
        
    return bar_list



def write_data(bar_list):
    """
    Writes DiveBar entries into an SQLite database
    """

    my_table = 'dive_bars_table'
    conn, c = sql_funcs.connect(SQL_FILE)

    for bar_tup in bar_list:
        bar_raw = bar_tup.name

        new_bar = bar_raw.strip("'")

        #check for pre-existing bars in the database (clumsy)
        c.execute(f"SELECT * FROM {my_table} WHERE name='{new_bar}'")
        old_bar = c.fetchall()

        if len(old_bar) > 0:
            print(f'{new_bar} already exists in database')
        else:
            new_bar_address = bar_tup.address
            new_bar_rank = bar_tup.rank
            new_bar_url = bar_tup.url
            SQL_str_1 = f"INSERT INTO {my_table} (name, address, rank, url) VALUES"
            SQL_str_2 = f"('{new_bar}', '{new_bar_address}', '{new_bar_rank}', '{new_bar_url}')"
            SQL_str = SQL_str_1 + SQL_str_2
            c.execute(SQL_str) 

    conn.commit()
    sql_funcs.close(conn)
    

def main():
    print(f'Retrieving webpage ...')
    raw_html = simple_get(GET_URL)

    if raw_html is not None:
        print(f'Extracting data ...')
        bar_list = extract_data(raw_html)
        print(f'Writing to database ...')
        write_data(bar_list)
    else:
        print(f'No data, stopping.')


if __name__ == '__main__':
    main()

