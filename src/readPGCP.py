from bs4 import BeautifulSoup
import requests
from datetime import datetime

from classes.Competition import Competition

def readPGCP():
    now = datetime.now()
    
    competitions = []
    for year in range(2015, now.year + 1):
        url = 'http://iowfox.co.uk/pgcp/index_' + str(year) + '.html'
        page_response = requests.get(url)
        page = str(BeautifulSoup(page_response.content, "html.parser"))
        
        # go to individual listings
        page = page[page.find('Individual listings'):]
        page = page.split('<p>')
        
        for i in range(len(page)):
            page[i] = page[i].split('\n')
            
        data = page[1:] # remove first irrelevant entry
        
        for comp in data:
            C = Competition()
            
            splitAt = comp[1].find(',')
            C.SetName(comp[1][:splitAt])
            C.SetLocation(comp[1][splitAt + 2 :])
            try:
                date = comp[3]
                if (date.find('[') != -1):
                    date = date[: date.find('[')]
                if (date.find('(') != -1):
                    date = date[: date.find('(')]
                date = date.replace(',', '').replace('.', '').split(' ')
                
                if (date[2] == 'April'):
                    date[2] = 'Apr'
                elif (date[2] == 'June'):
                    date[2] = 'Jun'
                elif (date[2] == 'July'):
                    date[2] = 'Jul'
                elif (date[2] == 'Sept'):
                    date[2] = 'Sep'
                elif (date[2] == 'August'):
                    date[2] = 'Aug'
                    
                if (len(date) == 7):
                    date.append(str(year))
                    
                comp_start = datetime.strptime(date[1] + '-' + date[2] + '-' + date[7], '%d-%b-%Y')
                C.SetStartDate(comp_start)
                
                if (date[6] == 'April'):
                    date[6] = 'Apr'
                elif (date[6] == 'June'):
                    date[6] = 'Jun'
                elif (date[6] == 'July'):
                    date[6] = 'Jul'
                elif (date[6] == 'Sept'):
                    date[6] = 'Sep'
                elif (date[6] == 'August'):
                    date[6] = 'Aug'
                comp_end = datetime.strptime(date[5] + '-' + date[6] + '-' + date[7], '%d-%b-%Y')
                C.SetEndDate(comp_end)
            except:
                print('Failed to add comp:')
                print(comp)
                continue
            
            if (comp[5].find('ahref') != -1):
                url = comp[5].split('"')
                C.SetUrl(url[1])
            
            C.SetSport(0)
            competitions.append(C)
            
    return competitions