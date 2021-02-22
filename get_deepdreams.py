import requests, os, urllib
from bs4 import BeautifulSoup

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
dream_url = "https://deepdreamgenerator.com/u/304643"

# Step 1: Get the first dream page, determine how many dreams I have
page = requests.get(dream_url)

# Debug what we got - should say <Response [200]> if successful
print(str(page))

# Step 2: Use BeautifulSoup 2 parse le page
soup = BeautifulSoup(page.content, 'html.parser')

# Debug what soup got
# This is YUGE so uncomment if you dare.
#print(soup)

# Step 3: Get number of dreams I have
# Looks like it's contained in a span with the class 'counter-box'
counter_box = soup.find('span', class_='counter-box')
number_of_dreams = int(counter_box.text)

# If that worked, I should see '214' print as of 2/21/2021 9pm
print("Number of dreams I has: %d" % number_of_dreams)

# Divide number of dreams by 24, round up - that's the max number of
# pages we should attempt to scrap
number_of_pages = round(number_of_dreams / 24)
print("We should parse %d pages me thinks..." % number_of_pages)

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
    if page == 1:
        cur_dream_url = dream_url
    else:   
        cur_dream_url = dream_url + "?page=" + str(page_num)

    print("cur_dream_url is: %s" % cur_dream_url)

    # Step 1: Get the dream page
    page = requests.get(cur_dream_url)

    # Step 2: Use BeautifulSoup 2 parse the dream page
    soup = BeautifulSoup(page.content, 'html.parser')

    # Step 3: Get list of dreams
    dreams = soup.find_all('div', class_='item')

    # Counter to monitor number of dreams per page
    # Testing shows max of 24 dreams per page, but could be less due to incomplete pages
    dream_count=0

    # Step 4: Get list of dream img URLs
    for dream in dreams:
        # Debug the dreams
        #print(dream)
        img_html = dream.find('img', class_='light-gallery-item')

        # Debug the img
        #print(img_html)

        # Ok, that worked, we have the imgs! Now just save off the data-src
        # for each one - that's our img url :-)
        img_url = img_html['data-src']

        # This currently works - gets a list of dreams. WOO.
        print(img_url)

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
print("Found %d number of 'real dreams" % number_of_dreams)
print("We previously thought there would be %d dreams" % real_number_of_dreams)

# Now that we have a list of img URLs, download them to an img directory
# First, make sure an "img" directory exists
downloads_dir = "img"
does_dir_exist = os.path.isdir(downloads_dir)

if does_dir_exist is False:
    print("Making the %s directory..." % downloads_dir)
    os.mkdir(downloads_dir)
else:
    print("%s directory already exists :)" % downloads_dir)

# Debugging: does our list contain the same number of URLs?
print("img_urls contains %d img urls" % len(img_urls))

# Second, download all the images
for img_url in img_urls:
    name = os.path.basename(img_url)
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

# At this point, we should have all the dreams nicely downloaded
# Since we skip dreams already downloaded, this shouldn't take long to run
# after publishing new dreams. niace!
print("Hopefully all your dreams have come true!")
