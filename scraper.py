# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests, json

base_url = "http://www.sis.itu.edu.tr/tr/ders_programlari/LSprogramlar/prg.php"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def get_lecture_list():
    
    """
    Returns a list of available lecture codes. To do that, it scrapes the selection
    menu where students can choose different lecture codes and see the lectures
    opened in the current term with that lecture code.
    """
    
    # Collect the page
    page = requests.get(base_url, headers = headers)

    # Create a BeautifulSoup object an parse the page
    soup = BeautifulSoup(page.text, "html.parser")
    
    # Options will hold the possible values students can select on the webpage    
    options = soup.find("select").contents
    
    # We will get the lecture codes from those possible options
    lecture_codes = list()

    for i in range(2, len(options)):
        try:
            lecture_codes.append(options[i].get("value"))
        except:
            # There is an empty character between options
            continue
        
    with open("lecture_codes.txt", "w") as txt_file:
        txt_file.write(str(lecture_codes))
        
    return lecture_codes
    
def get_capacity_crn(lecture_codes):
    
    """
    Takes a list of strings(lecture codes) and scrapes the webpages
    for those codes.
    
    Returns a list of crns where (capacity - enrollment) > 0.
    """    
    
    crn_list = list()
    
    for lecture in lecture_codes:
        # Get the url for this one
        url = base_url + "?fb=" + lecture
        page = requests.get(url, headers = headers)
        soup = BeautifulSoup(page.text, "html.parser")
        
        tab_con = soup.find_all("td")
        
        # Since the document is unstructured, we have to use some 'magic' numbers
        # 34 is the first td where CRN's start and we get a new CRN every 14 tds.
        # 8 tds after the CRN we get course capacity and the next one after the course
        # capacity is the number of enrolled students
        for i in range(34, len(tab_con), 14):
            if (i + 9) > len(tab_con):
                break
            try:
                crn = str(tab_con[i]).lstrip("<td>").rstrip("</td>")
                capacity = str(tab_con[i + 8]).lstrip("<td>").rstrip("</td>")
                enrolled = str(tab_con[i + 9]).lstrip("<td>").rstrip("</td>")
                if (int(capacity) - int(enrolled)) > 0:
                    crn_list.append(crn)
            except: 
                break 
            
    return crn_list