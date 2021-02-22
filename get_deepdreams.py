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
print(soup)
