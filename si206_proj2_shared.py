from bs4 import BeautifulSoup
import re
import os
import csv
import unittest


# function 1
def load_listing_results(html_file): 
    """
    INPUT: A string containing the path of the html file
    RETURN: A list of tuples
    """
    with open(html_file, "r", encoding="utf-8-sig") as file:
        soup = BeautifulSoup(file, 'html.parser')
    # print(f"soup is {soup}")    
    
    # init listings list
    # find all div tags with datatestid=listing-card-title
    # append all the text of all of those to listings -- those are the names of the listings
    listings = []
    divs = soup.find_all('div', {"data-testid" : "listing-card-title"})
    for div in divs:
        listing = div.text
        listings.append(listing)
    print(f"listings is {listings}")
    print(f"length of listings is {len(listings)}")

    # init all_ids list and urls list
    # find all links
    # append all links to urls
    all_ids = []
    urls = []
    links = soup.find_all('a', href=True)
    for link in links:
        url = link.get('href')
        urls.append(url)
        # print(f"url is {url}")
    
    # make id re pattern
    # go through each url and only append to ids list if it matches 
    id_pattern = r"/rooms/(?:plus/)?(\d+)"
    for url in urls:
        id_match = re.findall(id_pattern, url)
        
        if id_match:
            all_ids.extend(id_match)
    print(f"ids is {all_ids}")
    print(f"length of all_ids is {len(all_ids)}")
    
    # remove id dupes
    # make list of tuples
    ids = list(set(all_ids))
    print(f"length of ids without duplicates is {len(ids)}")
    tups = list(zip(listings, ids))    
    print(f"\ntups is {tups}")
    print(f"length of tups is {len(tups)}")
    return tups
    pass