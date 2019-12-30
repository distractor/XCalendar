from bs4 import BeautifulSoup
import requests
from datetime import datetime

from classes.Competition import Competition

def readLivetrack24():

    competitions = []
    # read from URL
    url = 'https://www.livetrack24.com/events/'
    page_response = requests.get(url)
    page = BeautifulSoup(page_response.content, 'html.parser')
    data = page.find_all(class_ = 'event-item')

    for comp in data:
        C = Competition()
        
        comp_name = comp.find(class_ = 'eventH2banner').string
        C.SetName(comp_name)
        
        comp_url = 'https://www.livetrack24.com' + comp.find('a').get('href')
        C.SetUrl(comp_url)
        
        childs = []
        for child in comp.find(class_ = 'informationOverlay').descendants:
            if (child.string not in childs) and (child.string != None):
                childs.append(child.string.replace('\t', '').replace('\r', '').replace('\n', ''))

        comp_location = childs[1]
        C.SetLocation(comp_location)
        
        date = childs[4]
        date = date.split(' ')
        try:
            if (len(date) > 6):
                comp_start = datetime.strptime(date[0] + "-" + date[1] + "-" + date[2], '%d-%b-%Y')
                comp_end = datetime.strptime(date[4] + "-" + date[5] + "-" + date[6], '%d-%b-%Y')
            elif (len(date) == 6):
                comp_start = datetime.strptime(date[0] + "-" + date[1] + "-" + date[-1], '%d-%b-%Y')
                comp_end = datetime.strptime(date[3] + "-" + date[4] + "-" + date[-1], '%d-%b-%Y')
            else:
                comp_start = datetime.strptime(date[0] + "-" + date[-2] + "-" + date[-1], '%d-%b-%Y')
                comp_end = datetime.strptime(date[2] + "-" + date[-2] + "-" + date[-1], '%d-%b-%Y')
        except:
            print("Something went wrong when reading dates of %s." % comp_name)
            print("Date array: ", date)
            
        C.SetStartDate(comp_start)
        C.SetEndDate(comp_end)
        
        comp_sport = childs[-2]
        if (comp_sport == 'Paraglider'):
            C.SetSport(0)
        else:
            C.SetSport(-1)
            
        competitions.append(C)

    return competitions
