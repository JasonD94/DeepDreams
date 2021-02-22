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

# Step 1: Get the first dream page to debug it
page = requests.get(dream_url)

# Debug what we got
print(str(page))

# Step 2: Use BeautifulSoup 2 parse le page
soup = BeautifulSoup(page.content, 'html.parser')

# Debug what soup got
#print(soup)

# Looks like I want:
# div ddg-type="dream" -> div -> div -> img -> data-src
# Should be a URL pointing to the dream.
# Maybe class item will work to get the dreams?

dreams = soup.find_all('div', class_='item')

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
    print(img_url)
    
    count += 1

# Appears to be 24 dreams per page.
# So we can do basic math - number of dreams I have, divided by 24
# And that should *roughly* get me the number of pages to look at!
print("Found %d dreams!" % count)
