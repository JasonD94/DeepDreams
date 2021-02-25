import requests, os, urllib, math
from bs4 import BeautifulSoup

#
# Will be web scrapping my Deep Dream Generator public dreams, from:
# https://deepdreamgenerator.com/u/304643
# Different pages, currently going up to page 9 like:
# https://deepdreamgenerator.com/u/304643?page=9
# Trying to hit page=10 displays an error saying:
#
# Empty
# You have not made any public Dreams yet.
# You can go to your Dreams and start publishing some of them.
#

#
# ¡¡¡ NOTE: !!!
# DO NOT SCRAP MY DREAMS, that goes against DeepDreamGenerator's guidelines:
# https://deepdreamgenerator.com/info
#
# However, I feel like I SHOULD be allowed to download my own dreams, hence this script.
# Thus, please change the username to your own account before running this script!
#
#	Thought: could also append "/best" to get a list of dreams in order of rating
#
username = "304643"
dream_url = "https://deepdreamgenerator.com/u/" + username
login_url = "https://deepdreamgenerator.com/login"

"""
        If using the "/best" sorting option, you MUST log into Deep Dream Generator
        Following this site's recommendation on how to log in using Python + Requests
        so we can still download dreams. :-)

        (side idea/note: if this works, I could download dreams I HAVEN'T PUBLICALLY
         POSTED... ooo that would be super helpful and cool!)

        https://towardsdatascience.com/scraping-data-behind-site-logins-with-python-ee0676f523ee
"""

session = requests.Session()

# Get the login page so we can get the token from the page
login_page = session.get(login_url)

# Parse out the token - it's under an input with the name '_token'
login_soup = BeautifulSoup(login_page.content, 'html.parser')
token = login_soup.find('input', {'name': '_token'}).get('value')

# obviously NOT publishing these details to Github nor do I recommend ANYONE do such a thing on purpose...
payload = {'email': '>>this_would_be_your_email<<',
           'password': '>>this_would_be_your_password<<',
           '_token': token}

#print("Token might be: %s" % token)
#print("payload: %s" % payload)

# Try to post the payload to deep dream generator so we can log in
s = session.post(login_url, data=payload, headers = dict(referer=login_url))

# Step 0: Do we want to download dreams by latest or best sorting?
# If we pick latest, we should name the dream based on date it was added
# If we pick best, we should name the dreams like "dream_num1.jpg", "dream_num2",
# etc where 1 == #1 dream, 2 == #2 dream, etc.
print("¡¡¡¡ WARNING: only download dreams you personally created !!!!\n\n")
print("** Deep Dream Generator Downloader V1.0 **")
print("Enter 1 for latest dream sorting download, or 2 for best dream sorting download: ")
sorting_type = ""

while sorting_type is not "1" and sorting_type is not "2":
    sorting_type = input()

    if sorting_type is not "1" and sorting_type is not "2":
        print("\nError: invalid sorting type. ")
        print("Please enter 1 for latest dream sorting download, or 2 for best dream sorting download")

if sorting_type is "2":
    dream_url = dream_url + "/best"

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

# So counter box is different or something for the 'best' page... hmm, debug!
# Update: /best/ requires a login... blah...
print(counter_box)

number_of_dreams = int(counter_box.text)

# If that worked, I should see '214' print as of 2/21/2021 9pm
print("Number of dreams I has: %d" % number_of_dreams)

# Divide number of dreams by 24, AND ALWAYS round up [ hence math.ceil() ]
# Since we want 9.1 to turn into Page 10, not Page 9
number_of_pages = math.ceil(number_of_dreams / 24)
print("We should parse %d pages I thinks...\n" % number_of_pages)

# Counter to make sure we got the right amount of dream urls
real_number_of_dreams = 0

# List of all the dream img urls for mass downloading later on
img_urls = []

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
    dream_count=0

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
print("\nFound %d number of 'real' dreams" % number_of_dreams)
print("We previously thought there would be %d dreams" % real_number_of_dreams)

# Debugging: does our list contain the same number of URLs?
print("img_urls contains %d img urls\n" % len(img_urls))

# Now that we have a list of img URLs, download them to an img directory
# First, make sure an "img" directory exists
downloads_dir = "img"

# Using a separate dir for best dream sorting download
if sorting_type is "2":
    downloads_dir = "best_dreams"

does_dir_exist = os.path.isdir(downloads_dir)

if does_dir_exist is False:
    print("Making the %s directory..." % downloads_dir)
    os.mkdir(downloads_dir)
else:
    print("%s directory already exists :)" % downloads_dir)

dream_count=1

# Second, download all the images
for img_url in img_urls:
    name = os.path.basename(img_url)
    filename = os.path.join(downloads_dir, name)

    # If sorting by best, then filename should be "dream_num###.jpg"
    # instead of whatever randomly generated filename DeepDreamGenerator uses
    if sorting_type is "2":
        name = "dream_num" + str(dream_count) + ".jpg"
        filename = os.path.join(downloads_dir, name)

    if not os.path.isfile(filename):
        print("Downloading: %s to %s" % (name, filename))
        
        try:
            urllib.request.urlretrieve(img_url, filename)
            
        except Exception as exception:
            print(exception)
            print("Encountered unknown error when trying to download %s. Continuing." % filename)
    else:
        print("%s already downloaded!" % filename)

    dream_count += 1

# At this point, we should have all the dreams nicely downloaded
# Since we skip dreams already downloaded, this shouldn't take long to run
# after publishing new dreams. niace!
print("\n\nHopefully all your dreams have come true!")
