from bs4 import BeautifulSoup
import requests
from datetime import datetime
import json

from classes.Competition import Competition

def readAirtribune():
    # read URL
    url = 'https://airtribune.com/events/next' # read from this url
    page_response = requests.get(url)
    page = BeautifulSoup(page_response.content, 'html.parser')
    
    # Parsing JSON
    json_comps = str(page.find_all('script')[2]).split(';')[0]
    N = json_comps.find('{')
    json_comps = json_comps[N-1:]
    comps = json.loads(json_comps)
    
    c = comps['past-events']['content']
    for comp in comps['current-events']['content']:
        c.append(comp)
    for comp in comps['next-events']['content']:
        c.append(comp)
        
        
    competitions = []
    for comp in c:
        C = Competition()
        
        C.SetName(comp['title'])
        
        C.SetTimezone(comp['timezone'])
        
        date = comp['start_date'].split('-')
        comp_start = datetime.strptime(date[2] + '-' + date[1] + '-' + date[0], '%d-%m-%Y')
        C.SetStartDate(comp_start)
        
        date = comp['end_date'].split('-')
        comp_end = datetime.strptime(date[2] + '-' + date[1] + '-' + date[0], '%d-%m-%Y')
        C.SetEndDate(comp_end)
        
        C.SetCountry(comp['country']['name'])
        
        C.SetLocation(comp['place'])
        
        C.SetLatitude(comp['lat'])
        C.SetLongitute(comp['lon'])
        
        comp_url = 'https://airtribune.com' + comp['url']
        C.SetUrl(comp_url)
        
        C.SetSport(comp['sport'])

        competitions.append(C)
        
    return competitions