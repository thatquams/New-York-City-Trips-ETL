from access_nyc import access_nyc_data
import logging
import requests
from access_nyc import NYC_BASE_URL

# configure logging format output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)    

@access_nyc_data
def trips_record_data_links(nyc_data_content):
    
    expand_section = nyc_data_content.find('div', class_='faq-controls').find('a', class_='faq-expand-all').get('href')
    
    # result = requests.get(expand_section)
    headers = {
    "User-Agent": "Mozilla/5.0"
    }
    
    response = requests.get("""https://c.go-mpulse.net/api/config.json?key=QMXLB-WG9C2-LTK58-FW2PB-6ST8X&d=www.nyc.gov&\
                            t=5884078&v=1.632.0&if=&sl=0&si=jjymkg6opa-t6yuo7&plugins=AK,ConfigOverride,Continuity,\
                                PageParams,IFrameDelay,AutoXHR,SPA,Angular,Backbone,Ember,History,RT,CrossDomain,BW,\
                                    PaintTiming,NavigationTiming,ResourceTiming,Memory,CACHE_RELOAD,Errors,TPAnalytics,\
                                        UserTiming,Akamai,LOGN&acao=&ak.ai=181928
                                        """, headers=headers)
    
    print(response.status_code)
    
    
    return response.content


result = trips_record_data_links()
print(result)
    
    
# https://data.cityofnewyork.us/api/v3/views/u253-aew4/query.json