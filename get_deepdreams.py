import requests, os, urllib, math, secrets
from bs4 import BeautifulSoup

"""
    HOW TO USE THIS SCRIPT:

    1. Add a "secrets.py" file with your DDG login credentials (see the comment above the definition
       of the username/email/password variables)
    2. Run this script (in IDLE, hit F5)
    3. Type a number between 1 and 4 into the console. The options are straight forward; they're just
       how you'd like the dreams to be sorted by. Options are 'latest', 'best', and 'all'. All includes
       non-public dreams too, and is basically the 'latest' sorting but includes non-public dreams.
       Option '4' is all of the above run one by one (could parallize this but might annoy DDG and I think
       they only like one auth at a time, so best not to do this without asking them nicely)
    4. Sit back and watch your dreams come true. Dreams get downloaded into directories where ever this script
       lives. Directories include 'latest_dreams' (option 1), 'best_dreams' (option 2) and
       'all_dreams' (option 3). Option 4 will populate all of these directories for you. :)

    NOTEs:

    'DDG' => DeepDreamGenerator

    TODOs:

    - Make a command line option for username, email, and password
    - More error checking
    - Rework the script so it isn't a giant 300 line file, I made get_deep_dreams() as a hacky work
      around to add option 4 (which runs all sorting options)
    - Probably should ask DDG if this is really okay, but but now they haven't yelled at me or banned me
      Also now I have my dreams so I don't really care if they ban me but I would be really sad if they did
      (DDG if you're reading this, I tried to follow your rules, plz don't ban me ok?)
"""

#
# ¡¡¡ NOTE: !!!
# DO NOT SCRAP MY DREAMS, that goes against DeepDreamGenerator's guidelines:
# https://deepdreamgenerator.com/info
#
# However, I feel like I SHOULD be allowed to download my own dreams, hence this script.
#
# Thus, you MUST user your own user credentials to run this script. I no longer include
# mine and my secrets.py file is .gitignore'd so make sure to make a DDG account to
# take full advantage of this script
#

"""
********************************************************************************
* Note: using another .py file called "secrets.py" that is hidden from Git/GitHub
*         If you wish to use this script with the "/best" or "all" filters, you'll
*       need to provide credentials for your Deep Dream Generator account in the
*       "secrets.yaml" file. You'll need to create it yourself in the format:
*
*   email: your@email.com
*   password: your_password
*   username: your_ddg_username
*
*   Based on: https://stackoverflow.com/a/25501861
*
********************************************************************************
"""
username = secrets.username
email = secrets.email
password = secrets.password

dream_url = "https://deepdreamgenerator.com/u/" + username
login_url = "https://deepdreamgenerator.com/login"

"""
        If using the "/best" sorting option, you MUST log into Deep Dream Generator
        Following this site's recommendation on how to log in using Python + Requests
        so we can still download dreams. :-)

        https://towardsdatascience.com/scraping-data-behind-site-logins-with-python-ee0676f523ee

        Some other very helpful articles/posts:
        https://kazuar.github.io/scraping-tutorial/
        https://stackoverflow.com/a/25284165
"""

session = requests.Session()

# Get the login page so we can get the token from the page
login_page = session.get(login_url)

# Parse out the token - it's under an input with the name '_token'
login_soup = BeautifulSoup(login_page.content, 'html.parser')
token = login_soup.find('input', {'name': '_token'}).get('value')

# Obviously NOT publishing these details to Github nor do I recommend ANYONE do such a thing on purpose...
payload = {'email': email,
           'password': password,
           '_token': token}

# Try to post the payload to deep dream generator so we can log in
s = session.post(login_url, data=payload, headers = dict(referer=login_url))

# Get the largest dream page number - used to estimate how many dreams we
# might be downloading
def get_largest_page_number(pagination_ul_list):
    max_page = 0
   
    for pagination_element in pagination_ul_list:
        if pagination_element is not None:
            try:
                if int(pagination_element.text) > max_page:
                    max_page = int(pagination_element.text)
            except:
                # A few of the pagination elements aren't valid integers
                # Examples: < ... >
                # So just ignore them.
                #print("Invalid page number found for %s" % pagination_element)
                continue

    return max_page

# Get all the URLs to download images off of
def get_img_urls(number_of_pages):

    img_urls = []

    # Counter to make sure we got the right amount of dream urls
    real_number_of_dreams = 0

    # Now we can loop over all the deep dream pages.
    # We have the number of pages from parsing the first page.
    # Number of pages is currently 9, so this loop should go pages 1 to 9
    # +1 because range doesn't include the end value
    for page_num in range (1, int(number_of_pages) + 1):

        # I deleted the copy/pasta code, so now this loop handles all dreams
        # Thus, must handle the edge case of first page not having a ?page=
        # in the dream page URL
        cur_dream_url = ''
        
        if page_num == 1:
            cur_dream_url = dream_url
        else:   
            cur_dream_url = dream_url + "?page=" + str(page_num)

        print("cur_dream_url is: %s" % cur_dream_url)

        # Step 1: Get the dream page
        # Step 2: Use BeautifulSoup 2 parse the dream page
        # Step 3: Get list of dream
        # NOTE: probably fine using requests here, but if that breaks, switch to 'session' instead
        dream_page = session.get(cur_dream_url)
        dream_soup = BeautifulSoup(dream_page.content, 'html.parser')
        dreams = dream_soup.find_all('div', class_='item')

        # Counter to monitor number of dreams per page
        # Testing shows max of 24 dreams per page, but could be less due to incomplete pages
        dream_count = 0

        # Step 4: Get list of dream img URLs
        for dream in dreams:

            # Find the img's HTML
            img_html = dream.find('img', class_='light-gallery-item')

            # Ok, that worked, we have the imgs! Now just save off the data-src
            # for each one - that's our img url :-)
            img_url = img_html['data-src']
            img_urls.append(img_url)
            
            dream_count += 1
            real_number_of_dreams += 1

        # At this point, we're done for the current page.
        # Let's check how many dreams we got for the page though
        print("Found %d dreams for page %d!" % (dream_count, page_num))

        # Debugging - add a break here if things break, so you don't go through
        # all the pages just to find out something broke with the img downloading code.
        #break;

    # Some debugging checks
    # Should have gotten the same number of dreams as seen previously
    # So number_of_dreams should equal real_number_of_dreams
    print("\nFound %d dreams over %d pages" % (real_number_of_dreams, int(number_of_pages)))
    return img_urls

# Given a sorting type and an list of image URLs, this function downloads all of the
# images which haven't been previously downloaded before
def download_all_dreams(downloads_dir, sorting_type, img_urls):

    dream_count = 1
    dream_downloaded = 1
    dream_errors = 0

    # Second, download all the images
    for img_url in img_urls:
        name = os.path.basename(img_url)
        filename = os.path.join(downloads_dir, name)

        # If sorting by best, then filename should be "dream_num###.jpg"
        # instead of whatever randomly generated filename DeepDreamGenerator uses
        if sorting_type == "2":
            name = "dream_num" + str(dream_count) + ".jpg"
            filename = os.path.join(downloads_dir, name)

        if not os.path.isfile(filename):
            print("Downloading: %s to %s" % (name, filename))
            
            try:
                urllib.request.urlretrieve(img_url, filename)
                dream_downloaded += 1
                    
            except Exception as exception:
                print(exception)
                print("Encountered unknown error when trying to download %s. Continuing." % filename)
                dream_errors += 1
        else:
            print("%s already downloaded!" % filename)

        dream_count += 1

    # At this point, we should have all the dreams nicely downloaded
    # Since we skip dreams already downloaded, this shouldn't take long to run
    # after publishing new dreams. niace!
    print("\nFound %d dreams. Downloaded %d of them this run.\n" % (dream_count, dream_downloaded))
    print("NOTE: found %d errors when trying to download dreams.\n" % dream_errors)


""""
    Basically, this will get all the dreams at a given deepdreamgenerator URL.
    You can do:

    /        ==> latest dreams by default
    /best    ==> best dreams, sorted by the number of likes on DDG
    /account ==> latest dreams but also those that aren't public
"""

def get_deep_dreams():
    print("Dream url is: %s" % dream_url)

    # Step 1: Get the first dream page, determine how many dreams I have
    dream_page = session.get(dream_url)

    # Debug what we got - should say <Response [200]> if successful
    print(str(dream_page))

    # Step 2: Use BeautifulSoup 2 parse le page
    dream_soup = BeautifulSoup(dream_page.content, 'html.parser')

    # Debug what soup got
    # This is YUGE so uncomment if you dare.
    #print(dream_soup)

    # Step 3: Get number of dreams I have
    # Looks like it's contained in a span with the class 'counter-box'
    counter_box = dream_soup.find('span', class_='counter-box')

    print(counter_box)

    # Check for no counter_box; this is a tell tale sign we're stuck at the log in page for DDG...
    # If so, the safest option to warn the user & exit, instead of causing an exception on the next line.
    if counter_box is None:
        print("ERROR: log in to Deep Dream Generator Failed! Check your creds or maybe this script borked. :(")

        # Ye this is apparently not recommended but it doesn't quit the Idle shell on my Windows box so...
        raise SystemExit

    number_of_dreams = int(counter_box.text)

    # Divide number of dreams by 24, AND ALWAYS round up [ hence math.ceil() ]
    # Since we want 9.1 to turn into Page 10, not Page 9
    number_of_pages = math.ceil(number_of_dreams / 24)
    print("We should parse %d pages I thinks...\n" % number_of_pages)

    # For sorting_type "3", we'll have to grab the number of pages from the
    # "pagination" ul class. Note that these can be spans or hrefs! so don't
    # be too specific to beautifulsoup.
    pagination_ul_list = dream_soup.find_all(class_='page-link')
    max_page = get_largest_page_number(pagination_ul_list)

    # Debugging
    print("Looks like the number of pages should be %d" % max_page)

    # Only use max_page if we're downloading ALL of my dreams
    # Otherwise we'll stick to the tried & true counter_box
    if sorting_type == "3":
        number_of_pages = max_page

    # List of all the dream img urls for mass downloading later on
    img_urls = get_img_urls(number_of_pages)

    # Debugging: does our list contain the same number of URLs?
    print("Number of dreams we thought we might find: %d" % number_of_dreams)
    print("img_urls contains %d img urls\n" % len(img_urls))

    # Now that we have a list of img URLs, download them to an img directory
    # First, make sure an "img" directory exists
    downloads_dir = "latest_dreams"

    # Using a separate dir for best dream sorting download
    if sorting_type == "2":
        downloads_dir = "best_dreams"

    elif sorting_type == "3":
        downloads_dir = "all_dreams"

    does_dir_exist = os.path.isdir(downloads_dir)

    if does_dir_exist is False:
        print("Making the %s directory..." % downloads_dir)
        os.mkdir(downloads_dir)
    else:
        print("%s directory already exists :)" % downloads_dir)

    # Finally, download all of my dreams!
    download_all_dreams(downloads_dir, sorting_type, img_urls)

    print("Hopefully all your dreams have come true!")


# Step 0: Do we want to download dreams by latest or best sorting? Or all the dreams even non-public ones?
# If we pick latest, we should name the dream based on the DDG file name
# If we pick best, we should name the dreams like "dream_num1.jpg", "dream_num2",
# etc where 1 == #1 dream, 2 == #2 dream, etc.
# If we pick all, then we should just name dreams based on the DDG file name
print("¡¡¡¡ WARNING: only download dreams you personally created !!!!\n\n")
print("** Deep Dream Generator Downloader V1.1 **")
print("Enter 1 for latest dream sorting, 2 for best dream sorting, 3 for all dreams and 4 for all of these: ")
sorting_type = ""

while sorting_type != "1" and sorting_type != "2" and sorting_type != "3" and sorting_type != "4":
    sorting_type = input()

    if sorting_type != "1" and sorting_type != "2" and sorting_type != "3" and sorting_type != "4" :
        print("\nError: invalid sorting type. ")
        print("Enter 1 for latest dream sorting, 2 for best dream sorting, 3 for all dreams \
                     and 4 for all of these: ")

if sorting_type == "2":
    dream_url = dream_url + "/best"

elif sorting_type == "3":
    dream_url = dream_url + "/account"

elif sorting_type == "4":

    # Method 1 first, "latest" sorting
    # Make sure to set sorting_type so the rest of the script works; noticed directories weren't being
    # created when I ran this for the first time on a different machine. Opps!
    sorting_type = "1"
    dream_url = "https://deepdreamgenerator.com/u/" + username
    get_deep_dreams()

    # Method 2 second, "best" sorting
    sorting_type = "2"
    dream_url = "https://deepdreamgenerator.com/u/" + username + "/best"
    get_deep_dreams()

    # Finally Method 3, "all dreams even though not public"
    sorting_type = "3"
    dream_url = "https://deepdreamgenerator.com/u/" + username + "/account"
    get_deep_dreams()

    quit()  # Fin

# If we end up here, then options 1 - 3 were selected. So grab the requested dreams!
get_deep_dreams()
