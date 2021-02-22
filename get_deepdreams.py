import requests
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
number_of_dreams = counter_box.text

# If that worked, I should see '214' print as of 2/21/2021 9pm
print("Number of dreams I has: %s" % number_of_dreams)

# Divide number of dreams by 24, round up - that's the max number of
# pages we should attempt to scrap
number_of_pages = round(int(number_of_dreams) / 24)
print("We should parse %d pages me thinks..." % number_of_pages)


# Looks like finding all the 'items' will get us all the dreams
dreams = soup.find_all('div', class_='item')

# Curious how many dreams each page has.
# Turns out, it maxes out at 24. Could be less, like on the last page
# or if I didn't have 24 dreams total.
count=0

# Now that we have all the dreams, let's make a list of the img URLs
img_urls = []
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
    
    count += 1

# Appears to be 24 dreams per page.
# So we can do basic math - number of dreams I have, divided by 24
# And that should *roughly* get me the number of pages to look at!
print("Found %d dreams!" % count)

# Now we can loop over additional pages. We have the number of pages from parsing
# the first page. So if the number is >1, we should be good to run the above
# code a few times or whatever.
# Number of pages is currently 9, so this loop should go pages 2 to 9
# +1 because range doesn't include the end value
for page in range (2, int(number_of_pages) + 1):
    cur_dream_url = dream_url + "?page=" + str(page)
    print("cur_dream_url is: %s" % cur_dream_url)

    # Step 1: Get the dream page
    page = requests.get(cur_dream_url)

    # Step 2: Use BeautifulSoup 2 parse the dream page
    soup = BeautifulSoup(page.content, 'html.parser')

    # Step 3: Get list of dreams
    dreams = soup.find_all('div', class_='item')

    dream_count=0 # Counter to monitor number of dreams per page

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

    # At this point, we're done for the current page.
    # Let's check how many dreams we got for the page though
    print("Found %d dreams!" % dream_count)
