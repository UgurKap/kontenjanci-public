# -*- coding: utf-8 -*-

from datetime import datetime
import time, schedule
import scraper

crn_list = list()

def write_to_file(crn_list):
    
    """
    Writes the contents of the given list to a file.
    """
    
    with open("available_courses.txt", "w") as txt_file:
        txt_file.write(crn_list)

def scrape():
    
    """
    Uses the scraper.py to scrape necessary information from the ITU website.
    If there is available spot in the class, adds it to crn_list and saves it
    to a file.
    """
    
    time.sleep(5) # Wait 5 seconds for website to be updated
    crn_list = scraper.get_capacity_crn(scraper.get_lecture_list())
    write_to_file(str(crn_list))
    
# Scraping every 15 minutes
schedule.every().hour.at(":00").do(scrape)
schedule.every().hour.at(":15").do(scrape)
schedule.every().hour.at(":30").do(scrape)
schedule.every().hour.at(":45").do(scrape)

while True:
    schedule.run_pending()
    time.sleep(1)
