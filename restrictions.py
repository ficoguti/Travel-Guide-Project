import requests
from geocoding import getGeocode, getManyIATA
import pandas as pd
from config import AUTH_KEY



def getRestrictions(destination):
    
#     originCoords = getGeocode(origin)
    destCoords = getGeocode(destination)
    
#     originIATA = getIATA(originCoords)
    destIATA = getManyIATA(destCoords)
    

    URL = 'https://covid-api.thinklumo.com/data?airport='
    
    headers = {
        "x-api-key": AUTH_KEY
    }
    
    for iata in destIATA:
        decoder = requests.get(URL + iata, headers=headers)
        if decoder.status_code == 200:
            dJSON = decoder.json()

            return dJSON
    
    return None
    
    
def getAdvisoryDF(dJSON):
    df = pd.json_normalize(dJSON['travel_advisories'])
    
    FIELDS = ["issued_by", "advisory", "url", "last_updated"]
    
    return df[FIELDS]
    
    
def getChartURL(dJSON):
    return dJSON['covid_stats']['country']['chart_url']
  

def getRiskLevel(dJSON):
    return dJSON['covid_stats']['country']['risk_rating']['risk_level'].upper()

  
def getEntryExitDF(dJSON):
    df = pd.json_normalize(dJSON['covid_info']['entry_exit_info'])
    
    FIELDS = ["source", "quarantine", "testing", "travel_restrictions", "last_updated"]
    
    return df
  
  
def main():
    destination = input('Enter a destination: ')
    jsonResponse = getRestrictions(destination)
#     print(jsonResponse)
    if(jsonResponse is not None):
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
            print(getAdvisoryDF(jsonResponse))
            print(getEntryExitDF(jsonResponse))
        print("Covid Data Chart:", getChartURL(jsonResponse))
        print("Risk Level:", getRiskLevel(jsonResponse))
    else:
        print('No information could be retrieved.')
    

if __name__ == "__main__":
    main()