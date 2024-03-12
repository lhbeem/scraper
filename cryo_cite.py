#!/usr/bin/env python3


import requests
from bs4 import BeautifulSoup
import argparse

def page_cite(soup):
    content = soup.find_all('a', class_='article-title')
    for i in content:
        if 'href' in i.attrs:
              link = i.get('href')
              split = link.split('/')
              vol = split[4]
              page = split[5]
              year = split[6]
              metriclink = f'{link}/tc-{vol}-{page}-{year}-metrics.html'
              r2 = requests.get(metriclink)
              s2 = BeautifulSoup(r2.content, 'html.parser')
              
              crossref = s2.find_all('h3',class_='metrics-crossref-headline')
              if len(crossref) == 0:
                  cite = 0
              else:
                  cite = int( crossref[0].text.split()[0] )
      		
              print(page,cite)


def main(args):
    print
    for issue in range(1,13):
        r = requests.get(f'https://tc.copernicus.org/articles/{args.vol}/issue{issue}.html')
        soup = BeautifulSoup(r.content, 'html.parser')
        print (f'Volume:{args.vol} Issue:{issue}')
        page_cite(soup)
    
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='scrape crossref citations')

    parser.add_argument('vol', help= 'volume of cryosphere to scrap') 
    args = parser.parse_args()

    main(args)

