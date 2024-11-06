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


























# function 2
def get_listing_details(listing_id): 
    """
    INPUT: A string containing the listing id
    RETURN: A tuple
    """
    # open the file
    path = f"html_files/listing_{listing_id}.html"
    with open(path, "r", encoding="utf-8-sig") as file:
        soup = BeautifulSoup(file, "html.parser")

    # ######## policy number ########
    # init clean uls list
    # find first ul with class f19phm7j to get the policy number
    policy_num = ""
    all_lis = []
    lis = soup.find('li', class_="f19phm7j")
    for tag in lis:
        tag = lis.text
        all_lis.append(tag)
    # remove dupes
    all_lis = list(set(all_lis))
    print(f"all lis is {all_lis}")
    
    # regex pattern to match for policy number
    # search through string to get rid of policy number text
    policy_pattern = r"Policy number: ([\w\s-]+)"
    for li in all_lis:
        policy_match = re.search(policy_pattern, li)
        # print(f"li is {li}")
        # print(f"policy match is {policy_match}")

        if policy_match:
            policy_num = policy_match.group(1)
    print(f"\n\n--------\npolicy num is {policy_num}\n")



    # ######## superhost ########
    # search for span with class _1mhorg9 to find superhost flag
    # if not there set as regular
    superhost = ""
    span = soup.find('span', class_='_1mhorg9')
    sh_text = span.text
    if span:
        superhost = sh_text
        print(f"superhost found")
    else:
        superhost = "regular"
        print(f"superhost not found")
    print(f"superhost is {superhost}\n")



    # ######## host names ########
    # class _14i3z6h has name and place type
    # init blank hostnames string
    # define re search pattern for the word by
    # search through h2 with class _14i3z6h 
    host_names = ""
    by_pattern = r"\b(by)\b"
    h2 = soup.find('h2', class_='_14i3z6h')
    host_text = h2.text
    print(f"host_text is {host_text}")

    # use re to clean string -- find where "by" is and then slice from there
    # if match is found return names
    # if not return missing
    by_word = re.search(by_pattern, host_text)
    if by_word:
        by_start_index = by_word.start()
        host_names = host_text[(by_start_index+3):]
    else:
        host_names = "missing"
    print(f"host_names is {host_names}\n")



    # ######## place type ########
    # use same logic as last one to grab information
    # init 2 different search patterns for different criteria
    # (?i) makes match case insensitive
    place_type = ""
    private_pattern = r"(?i)private"
    shared_pattern = r"(?i)shared"
    h2 = soup.find('h2', class_='_14i3z6h')
    place_text = h2.text
    print(f"place_text is {place_text}")

    # use re to clean string -- find where "by" is and then slice from there
    # if match is found return names
    # if not return missing
    private = re.search(private_pattern, place_text)
    shared = re.search(shared_pattern, place_text)
    if private:
        place_type = "Private Room"
    elif shared:
        place_type = "Shared Room"
    else:
        place_type = "Entire Room"
    print(f"place_type is {place_type}\n")



    # ######## number of reviews ########
    # init empty number of reviews
    # search for span with class _1jlwy4xq
    # get text and use RE \d
    num_reviews = 0
    review_pattern = r"\d+"
    span = soup.find('span', '_1jlwy4xq')
    review_text = span.text
    print(f"review text is {review_text}")

    # need to use search and groups since it's a match object by default
    num = re.search(review_pattern, review_text)
    if num:
        num_reviews = int(num.group(0))
    print(f"num_reviews is {num_reviews}\n")



    # ######## nightly rate ########
    # same logic as reviews
    # init empty rate
    # search for span with class _tyxjp1
    # get text and use RE \d
    rate = 0
    rate_pattern = r"\d+"
    span = soup.find('span', '_tyxjp1')
    rate_text = span.text
    print(f"rate text is {rate_text}")

    # need to use search and groups since it's a match object by default
    num = re.search(rate_pattern, rate_text)
    if num:
        rate = int(num.group(0))
    print(f"rate is {rate}\n--------\n\n")

    return (policy_num, superhost, host_names, place_type, num_reviews, rate)