from bs4 import BeautifulSoup
import requests, urllib, os, json, argparse
import platform, datetime

op = ''
desc = "Articles scraper"

if(platform.system() == 'Windows'):
    os.system('cls')
if (platform.system() == 'Linux'):
    os.system('clear')


