from bs4 import BeautifulSoup
import requests
from datetime import datetime

from classes.Competition import Competition

def readPWCA():
    now = datetime.now()
    
    competitions = []
    for year in range(2000, now.year + 1):
        url = 'http://www.pwca.org/view/tour/' + str(year)
        page_response = requests.get(url)
        page = BeautifulSoup(page_response.content, "html.parser")
        tables = page.find_all(class_ = "views-table")
        
        for table in tables:
            if (table.find('caption').string.find("Selective") != - 1):
                # ignore leagues
                continue
            
            data = table.find_all("td", class_ = "views-field-title")
            comp_names = []
            comp_locations = []
            comp_urls = []
            for comp in data:
                compID = comp.find("a").string
                
                if (compID.find(" ::: ") != - 1):
                    compID = comp.find("a").string.split(" ::: ")
                    comp_names.append(compID[0])
                    comp_locations.append(compID[1])
                elif (compID.find(" - ") != - 1):
                    compID = comp.find("a").string.split(" - ")
                    comp_names.append(compID[0])
                    comp_locations.append(compID[1])
                else:
                    comp_names.append(compID)
                    comp_locations.append('')

                comp_urls.append('http://www.pwca.org/' + comp.find('a').get('href'))
    
            data = table.find_all(class_ = "date-display-range")
            comp_starts = []
            comp_ends = []
            for comp in data:
                date = comp.contents[0].string.split("/")
                comp_starts.append(datetime.strptime(date[0] + "-" + date[1] + "-" + date[2], '%d-%m-%Y'))
                date = comp.contents[2].string.split("/")
                comp_ends.append(datetime.strptime(date[0] + "-" + date[1] + "-" + date[2], '%d-%m-%Y'))
    
            for i in range(len(comp_names)):
                C = Competition()
                C.SetName(comp_names[i])
                C.SetUrl(comp_urls[i])
                if comp_locations[i] != '':
                    C.SetLocation(comp_locations[i])
                C.SetStartDate(comp_starts[i])
                C.SetEndDate(comp_ends[i])
                C.SetSport(0) 
                competitions.append(C)
                
    return competitions