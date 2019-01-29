from bs4 import BeautifulSoup
import urllib.request

url = 'https://www.morningstar.com'
f = urllib.request.urlopen(url)

soup = BeautifulSoup(f, 'html.parser')
print(soup.prettify())

