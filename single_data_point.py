import urllib.request
import scrapy
import pandas as pd
import re

# Trim html tags
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', str(raw_html))
  return cleantext

# Returns the selector object that xpaths will extract from
def create_selector(url):
    # get web page
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()

    # decode
    html = mybytes.decode("utf8")
    fp.close()

    # create selector object
    sel = scrapy.Selector(text=html)
    return sel

# # Target:  Fund Family = "North Square"
# <span class="Fl(end)" data-reactid="48">American Beacon</span>
ticker = 'AGHPX'
url = 'https://finance.yahoo.com/quote/'+ticker+'/profile?p='+ticker

# path = '//span[contains(text(),"Fund Family")]/following-sibling::span[0]'
# preceding-sibling::h2[. = 'Headline 1']

path = '//span/text()'

sel = create_selector(url)
print(url)
print('-----1. selector created')
extract = sel.xpath(path).extract()
print('-----2. extracted path')
# print('-----   extract:',extract)
print('-----   length =',len(extract))
clean_extract = cleanhtml(extract)
print('-----3. html cleaned')
# print('-----   data:',clean_extract)
