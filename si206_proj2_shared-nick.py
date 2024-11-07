from bs4 import BeautifulSoup
import re
import os
import csv
import requests
import unittest

# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"

An example of that within the function would be:
    open("filename", "r", encoding="utf-8-sig")

There are a few special characters present from Airbnb that aren't defined in standard UTF-8 (which is what Python runs by default). This is beyond the scope of what you have learned so far in this class, so we have provided this for you just in case it happens to you. Good luck!
"""

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
    id_search = re.compile(r"title_(\d+)")
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
        header = ["Listing Title", "Listing ID", "Policy Number", "Host Level", "Host Name(s)", "Place Type", "Review Number", "Nightly Rate"]
        writer.writerow(header)

        writer.writerows(sorted_data)
        # print(f"csv written!\n\n")
    
    # # printing to check file
    # with open(filename, "r") as file:
    #     reader = csv.reader(file)
    #     for row in reader:
    #         print(row)
    pass












































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
        
        # if doesn't match both, append info to list as a tuple
        if not lid_search_1 and not lid_search_2:
            # print(f"incorrect format")
            incorrect_pns.append((lid, hostnames, policy_number))
    # print(f"incorrect pns is {incorrect_pns}")
    return incorrect_pns
    pass 












































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
# print(google_scholar_searcher("airbnb hotel"))












































# TODO: Don't forget to write your test cases! 
class TestCases(unittest.TestCase):
    def setUp(self):
        self.listings = load_listing_results("html_files/search_results.html")






    def test_load_listing_results(self):
        # print(load_listing_results("html_files/search_results.html"))

        # check that the number of listings extracted is correct (18 listings)
        self.assertEqual(len(self.listings), 18)

        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(self.listings), list)

        # check that each item in the list is a tuple
        for tup in self.listings:
            self.assertEqual(type(tup), tuple, "item of type != tuple found")

        # check that the first title and listing id tuple is correct (open the search results html and find it)
        self.assertEqual(self.listings[0][1], '1944564', "first entry incorrect id")

        # check that the last title and listing id tuple is correct (open the search results html and find it)
        self.assertEqual(self.listings[-1][1], '467507', "last entry incorrect id")





    def test_get_listing_details(self):
        html_list = ["467507",
                     "1550913",
                     "1944564",
                     "4614763",
                     "6092596"]
        
        # call get_listing_details for i in html_list:
        listing_information = [get_listing_details(id) for id in html_list]

        # check that the number of listing information is correct
        self.assertEqual(len(listing_information), 5)
        for info in listing_information:
            # check that each item in the list is a tuple
            self.assertEqual(type(info), tuple)
            # check that each tuple has 6 elements
            self.assertEqual(len(info), 6)
            # check that the first four elements in the tuple are strings
            self.assertEqual(type(info[0]), str)
            self.assertEqual(type(info[1]), str)
            self.assertEqual(type(info[2]), str)
            self.assertEqual(type(info[3]), str)
            # check that the rest two elements in the tuple are integers
            self.assertEqual(type(info[4]), int)
            self.assertEqual(type(info[5]), int)

        # check that the first listing in the html_list has the correct policy number
        self.assertEqual(listing_information[0][0], "STR-0005349", "incorrect policy number for id 467507")

        # check that the last listing in the html_list has the correct place type
        self.assertEqual(listing_information[-1][-3], "Entire Room", "incorrect place type for id 6092596")

        # check that the third listing has the correct cost
        self.assertEqual(listing_information[2][-1], 181, "incorrect cost for id 1944564")






    def test_create_listing_database(self):
        # print(create_listing_database("html_files/search_results.html"))
        detailed_data = create_listing_database("html_files/search_results.html")

        # check that we have the right number of listings (18)
        self.assertEqual(len(detailed_data), 18)

        for item in detailed_data:
            # assert each item in the list of listings is a tuple
            self.assertEqual(type(item), tuple)
            # check that each tuple has a length of 8
            self.assertEqual(len(item), 8, "a tuple has incorrect length")

        # check that the first tuple is made up of the following:
        # ('Loft in Mission District', '1944564', '2022-004088STR', 'Superhost', 'Brian', 'Entire Room', 422, 181)
        self.assertEqual(detailed_data[0], ('Loft in Mission District', '1944564', '2022-004088STR', 'Superhost', 'Brian', 'Entire Room', 422, 181), "the listing database first tuple does not match")
        
        # check that the last tuple is made up of the following:
        # ('Guest suite in Mission District', '467507', 'STR-0005349', 'Superhost', 'Jennifer', 'Entire Room', 324, 165)
        self.assertEqual(detailed_data[-1], ('Guest suite in Mission District', '467507', 'STR-0005349', 'Superhost', 'Jennifer', 'Entire Room', 324, 165), "the listing database last tuple does not match")






    def test_output_csv(self):
        # call create_listing_database on "html_files/search_results.html"
        # and save the result to a variable
        detailed_data = create_listing_database("html_files/search_results.html")

        # call output_csv() on the variable you saved
        output_csv(detailed_data, "test.csv")
        # print(output_csv(detailed_data, "test.csv"))


        # read in the csv that you wrote
        csv_lines = []
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.csv'), 'r') as f:
            csv_reader = csv.reader(f)
            for i in csv_reader:
                csv_lines.append(i)

        # check that there are 19 lines in the csv
        self.assertEqual(len(csv_lines), 19)

        # check that the header row is correct
        # print(f"','.join(csv_lines[0]) is {','.join(csv_lines[0])}")
        self.assertEqual(",".join(csv_lines[0]), "Listing Title,Listing ID,Policy Number,Host Level,Host Name(s),Place Type,Review Number,Nightly Rate", "header does not match")

        # check that the next row is the correct information about Guest suite in San Francisco
        self.assertEqual(",".join(csv_lines[1]), "Guest suite in San Francisco,6092596,STR-0000337,Superhost,Marc,Entire Room,713,164", "first data line does not match")

        # check that the row after the above row is the correct infomration about Private room in Mission District
        self.assertEqual(",".join(csv_lines[2]), "Private room in Mission District,16204265,1081184,Superhost,Koncha,Private Room,520,127", "second data line does not match")






    def test_validate_policy_numbers(self):
        # call create_listing_database on "html_files/search_results.html"
        # and save the result to a variable
        detailed_data = create_listing_database("html_files/search_results.html")

        # call validate_policy_numbers on the variable created above and save the result as a variable
        invalid_listings = validate_policy_numbers(detailed_data)
        # print(invalid_listings)

        # check that the return value is a list
        self.assertEqual(type(invalid_listings), list)

        # check that the elements in the list are tuples
        for tup in invalid_listings:
            self.assertEqual(type(tup), tuple, "an element in the list is not a tuple")
        # and that there are exactly three element in each tuple
            self.assertEqual(len(tup), 3, "there's a tuple longer than len 3 in the list")

def main (): 
    detailed_data = create_listing_database("html_files/search_results.html")
    output_csv(detailed_data, "airbnb_dataset.csv")

if __name__ == '__main__':
    # main()
    unittest.main(verbosity=2)
