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
    # make search and pattern to search through all divs with re
    listings = []
    id_search = re.compile("title_(\d+)")
    id_pattern = r"title_(\d+)"
    divs = soup.find_all('div', id=id_search)
    # print(f"divs is {divs}")
    
    # iterate through all divs
        # id is equal to match group 1 of searching the str(div) with the pattern
        # name is equal to the text of the div
        # append both as a tuple
    for div in divs:
        # print(f"div is {div}")
        id = re.search(id_pattern, str(div)).group(1)
        name = div.text
        listings.append((name, id))
    # print(f"listings is {listings}")
    # print(f"length of listings is {len(listings)}")
    # print(f"type of listings is {type(listings)}\n\n--------")
    return listings
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
    # print(f"\n\n--------\nlisting id is {listing_id}\n")

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
    # print(f"all lis is {all_lis}")
    
    # regex pattern to match for policy number
    # search through string to get rid of policy number text
    policy_pattern = r"Policy number: ([\w\s-]+)"
    for li in all_lis:
        policy_match = re.search(policy_pattern, li)
        # print(f"li is {li}")
        # print(f"policy match is {policy_match}")

        if policy_match:
            policy_num = policy_match.group(1)
    # print(f"policy num is {policy_num}\n")



    # ######## superhost ########
    # search for span with class _1mhorg9 to find superhost flag
    # if not there set as regular
    superhost = ""
    span = soup.find('span', class_='_1mhorg9')
    # print(f"span is {span}")
    try:
        sh_text = span.text
        superhost = sh_text
        # print(f"superhost found")
    except AttributeError:
        superhost = "regular"
        # print(f"superhost not found")
    # print(f"superhost is {superhost}")


    # ######## host names ########
    # class hnwb2pb has name, but also other things have that class
    # init hostnames string as "missing"
    # define re search pattern to start on the word by and capture the name
    # iterate through all h2s with that class
        # only update hostnames if search is successful
    hostnames = "missing"
    host_pattern = r"\bby\b (.+)"
    h2s = soup.find_all('h2', class_='hnwb2pb')
    # print(f"h2s is {h2s}")
    for h2 in h2s:
        host_text = h2.text
        # print(f"host text is {host_text}")
        host_re = re.search(host_pattern, host_text)

        if host_re:
            hostnames = host_re.group(1)
            # print(f"\n--------\nmatch found, group(1) is {host_re.group(1)}\n--------")
        # print(f"host names is {hostnames}")



    # ######## place type ########
    # use class _14i3z6h to grab place type
    # init 2 different search patterns for different criteria
    # (?i) makes match case insensitive
    place_type = ""
    private_pattern = r"(?i)private"
    shared_pattern = r"(?i)shared"
    h2 = soup.find('h2', class_='_14i3z6h')
    place_text = h2.text
    # print(f"place_text is {place_text}")

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
    # print(f"place_type is {place_type}\n")



    # ######## number of reviews ########
    # init empty number of reviews
    # search for span with class _1jlwy4xq
    # get text and use RE \d
    num_reviews = 0
    review_pattern = r"\d+"
    
    try:
        span = soup.find('span', '_1jlwy4xq')
        review_text = span.text
        # print(f"span is {span}")
        # print(f"review text is {review_text}")
    # except block for the one file that's different(?????)
    except AttributeError:
        # print(f"different file format")
        span = soup.find('span', 'a8jt5op')
        review_text = span.text
        # print(f"span is {span}")
        # print(f"review text is {review_text}")

    # need to use search and groups since it's a match object by default
    num = re.search(review_pattern, review_text)
    if num:
        num_reviews = int(num.group(0))
    # print(f"num_reviews is {num_reviews}\n")



    # ######## nightly rate ########
    # same logic as reviews
    # init empty rate
    # search for span with class _tyxjp1
    # get text and use RE \d
    rate = 0
    rate_pattern = r"\d+"
    span = soup.find('span', '_tyxjp1')
    rate_text = span.text
    # print(f"rate text is {rate_text}")

    # need to use search and groups since it's a match object by default
    num = re.search(rate_pattern, rate_text)
    if num:
        rate = int(num.group(0))
    # print(f"rate is {rate}\n--------\n\n")

    return (policy_num, superhost, hostnames, place_type, num_reviews, rate)
    pass







































# function 3
def create_listing_database(html_file): 
    """
    INPUT: A string containing the path of the html file
    RETURN: A list of tuples
    """
    
    """
    - init master database --> empty list
    - need to call first function which takes in
    an html file and returns a list of tuples
        - call the load_listing_results function using
          the html_file parameter from this function
    - iterate over each tuple
        - each tuple contains (name, id)
          (name is tuple[0] id is tuple[1])
    - for each tuple, call get_listing_details
      which returns a tuple with all the info
    - join each main tuple with each G_L_D tuple
    - append to master list
    """

    database = []
    # names and ids list of tuples
    listing_results = load_listing_results(html_file)
    for listing in listing_results:
        id = listing[1]
        listing_details = get_listing_details(id)
        
        full_listing_info = listing + listing_details
        database.append(full_listing_info)
    # print(f"\n\n--------\ndatabase is:")
    # count = 0
    # for tup in database:
    #     print(f"{count}. {tup}")
    #     count+=1
    # print(f"\n--------\n\n")
    # print(f"database is\n{database}")
    return database
    pass




































# function 4
def output_csv(data, filename): 
    """
    INPUT: A list of tuples and a string containing the filename
    RETURN: None
    """

    # sort data
    # data is a list of tuples
    sorted_data = sorted(data, key=lambda x: x[6], reverse=True)
    # print(f"sorted data is {sorted_data}")
    
    # write to the file with the inputted filename
    with open(filename, "w", newline='') as file:
        writer = csv.writer(file)

        # make the header
        header = ["Listing Title", "Listing ID", "Policy Number", "Host Level", "Host Name(s)", "Place Type", "Review number", "Nightly Rate"]
        writer.writerow(header)

        writer.writerows(sorted_data)
        # print(f"csv written!\n\n")
    
    # # printing to check file
    # with open(filename, "r") as file:
    #     reader = csv.reader(file)
    #     for row in reader:
    #         print(row)
    pass













































# function 5
def validate_policy_numbers(data):
    """
    INPUT: A list of tuples
    RETURN: A list of tuples
    """
    
    # init search patterns
    policy_pattern_1 = r"20\d{2}-00\d{4}STR"
    policy_pattern_2 = r"STR-000\d{4}"

    # init list of incorrect numbers
    incorrect_pns = []
    for tup in data:
        lid = tup[1]
        policy_number = tup[2]
        hostnames = tup[4]

        # skip pending or empty
        if policy_number == "pending" or lid == "":
            continue

        # search for correct format
        lid_search_1 = re.search(policy_pattern_1, policy_number)
        lid_search_2 = re.search(policy_pattern_2, policy_number)
        
        # if doesn't match both, append info to list
        if not lid_search_1 and not lid_search_2:
            # print(f"incorrect format")
            incorrect_pns.append(lid)
            incorrect_pns.append(hostnames)
            incorrect_pns.append(policy_number)
    # print(f"incorrect pns is {incorrect_pns}")
    return incorrect_pns
    pass 
















































# function 6
# EXTRA CREDIT 
def google_scholar_searcher(query): 
    """
    INPUT: query (str)
    Return: a list of titles on the first page (list)
    * see PDF instructions for more details
    """
    
    # handle spaces
    if ' ' in query:
        query = query.replace(' ', '+')
        # print(f"updated query is {query}")

    # make soup and requests
    url = f"https://scholar.google.com/scholar?hl=en&as_sdt=0%2C23&q={query}&btnG="
    resp = requests.get(url)
    if resp.status_code == 200:
        html = resp.text
        soup = BeautifulSoup(html, 'html.parser')
    else:
        # invalid url
        print(f"invalid url")
        return
    
    # find all h3's with gs_rt
    # init list of titles and append text of those elements to that list
    titles = []
    h3s = soup.find_all('h3', class_="gs_rt")
    for h3 in h3s:
        # print(f"h3 is {h3}\n")
        title = h3.text
        titles.append(title)
        # print(f"title is {title}")

    for i in range(len(titles)):
        titles[i] = (titles[i].replace('[HTML]', '').replace('[PDF]', '')).strip()
    # print(f"titles is {titles}")
    return titles
    pass
print(google_scholar_searcher("airbnb hotel"))
