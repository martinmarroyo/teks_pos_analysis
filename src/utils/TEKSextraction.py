from urllib.request import urlopen, Request
import time
from bs4 import BeautifulSoup
import pandas as pd
from loguru import logger

def get_soup(url):
    """
    Extracts html from given url and returns a Soup object
    """
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    html = urlopen(Request(url, headers={'User-Agent': user_agent})).read()
    return BeautifulSoup(html, 'html5lib')


def get_knowledge(soup, tag):
    """
    Extracts the knowledge information from soup and returns it as a list ('ss' is for first page, 'no' for all others)
    """
    knowledge = []
    try:
        #First page only
        if tag == "ss":
            knowledge_tag = soup.find_all(tag)[1].contents[0]
            knowledge = [line.strip().replace('\r','').replace('\n','') for line in knowledge_tag.strings if line.startswith("(") and not line.startswith("(b")]
        #All other pages
        elif tag == "no": 
            knowledge_tag = soup.find_all(tag)
            knowledge = [line.contents[0].strip().replace('\r','').replace('\n','') for line in knowledge_tag]
    except IndexError:
        logger.info("Item not found. Continuing...")
    except Exception:
        logger.exception("An exception occurred while trying to parse a page. Continuing...")
    return knowledge
    

def extract_teks(base_url, chapter, rule):
    """
    Extracts the Knowledge and Skills for a single subject(chapter) and grade(rule) and returns 
    the data as a list
    """ 
    #Set up our url and get the html
    url_append = f"readtac$ext.TacPage?sl=R&app=9&p_dir=&p_rloc=&p_tloc=&p_ploc=&pg=1&p_tac=&ti=19&pt=2&ch={chapter}&rl={rule}"
    soup = get_soup(base_url+url_append)  
    #Put all of the first page contents into the knowledge master list
    knowledge_master = get_knowledge(soup,"ss")
    #Determine if there is another page. If so, get the page and extract the info from there
    next_page = soup.find_all(attrs={"name":"Continued"})
    has_next_page = len(next_page) >= 1
    if has_next_page:
        while (has_next_page):
            #Get the url
            next_pg_url = next_page[0]['href']
            #Adding a pause to not overload the server with requests
            time.sleep(5)
            #get the soup
            soup = get_soup(base_url+next_pg_url)
            #get the knowledge
            knowledge_list = get_knowledge(soup,"no")
            #append the knowledge to knowledge_master
            for line in knowledge_list:
                knowledge_master.append(line)
            #update next_page
            next_pg = soup.find_all(attrs={"name":"Continued"})
            has_next_page = len(next_pg) >= 1
    return knowledge_master

