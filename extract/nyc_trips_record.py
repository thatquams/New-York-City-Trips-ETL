from access_nyc import access_nyc_data
import logging
import requests
from access_nyc import NYC_BASE_URL
from datetime import datetime
import time

# configure logging format output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)    

@access_nyc_data
def trips_record_data_links(nyc_data_content):
    
    """
        Extract trip record download links for available NYC Taxi & Limousine Commission data.

        This function scrapes the monthly trip data links for each year shown in the TLC dataset
        section of the NYC Open Data portal. It processes the HTML returned by the `access_nyc_data`
        decorator, navigates through the year-specific FAQ sections, and extracts all anchor tags
        pointing to downloadable files (e.g., CSV, Parquet, or ZIP archives).

        It also logs progress for each month.

        Parameters
        ----------
        nyc_data_content : BeautifulSoup
            Parsed HTML content of the NYC TLC trip data page, automatically provided by
            the `access_nyc_data` decorator.

        Returns
        -------
        list
            A list containing all extracted download URLs for the target years.
    """
    data_urls = []
    
    # Build a list of years from 2009 up to the current year as the data collection started in `2009`, then sort descending

    all_data_year = list(range(2009, datetime.now().year + 1))
    sorted_data_year = sorted(all_data_year, reverse=True)
    
    try:
        for year in sorted_data_year:
            
            # Locate the HTML section for this year's data (div id="faq2024")
            get_expanded_section_content = nyc_data_content.select_one(f"div#faq{year}")
            
            if not get_expanded_section_content:
                logger.warning(f"Could not find data section for year {year}")
                continue
            
            # Extract the main table containing monthly download links
            table_contents_body = (
                                get_expanded_section_content
                                   .select('table tbody tr[valign="top"] > td')
                                )
            
            if not table_contents_body:
                logger.warning(f"No table contents found for year {year}")
                continue
 
            # Iterate through each <td> representing a month
            for td in table_contents_body:
                
                month = td.select_one('strong')
                month_name = month.get_text(strip=True) if month else "Unknown"

                # Extract href values and store them
                for link in td.select("a[href]"):
                    data_urls.append(link["href"])


                logger.info(f"Captured trip records for: {month_name}, {year}")

        return data_urls

    except Exception as e:
        logger.error(f"An error occurred while processing trip records: {e}")
        return []
    
    
    
result = trips_record_data_links()
print(result)