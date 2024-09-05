from bs4 import BeautifulSoup
import requests, urllib, os, json, argparse
import platform, datetime

op = ''
desc = "Articles scraper"

if(platform.system() == 'Windows'):
    os.system('cls')
if (platform.system() == 'Linux'):
    os.system('clear')

argp = argparse.ArgumentParser(usage = "scraper.py -t TYPE -q QUERY -c [COUNT]")
argp.add_argument("-t","--type",required= True)
argp.add_argument("-q","--query",required= True)
argp.add_argument("-c","--count")
argp.add_argument("-o","--output")
parser = argp.parse_args()
type = parser.type
query = parser.query
count = parser.count
output = parser.output
if(count == None): count = '10'

