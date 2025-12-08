from access_nyc import access_nyc_data
import logging
import requests
from access_nyc import NYC_BASE_URL

# configure logging format output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@access_nyc_data
def extract_nyc_meta_lookup_data(nyc_data_content, value:int=2) -> list:
    
    """
        Extracts all official NYC TLC metadata and lookup-table download links from the
        designated HTML section of the TLC website.

        This function is part of the metadata-ingestion layer of the NYC Taxi ETL pipeline,
        where accurate and up-to-date reference files are essential for business-critical analytics.

        Specifically, this function traverses the first two <ul> elements of the TLC resources
        section—where the commission publishes structured download links for:

            • Yellow / Green / FHV / HVFHV Trip Data Dictionaries  
            • Trip Record User Guide  
            • PARQUET-format documentation  
            • Taxi Zone Lookup Table (CSV)  
            • Taxi Zone Shapefile (PARQUET)  
            • Taxi Zone reference maps for NYC boroughs  

        Each extracted hyperlink is normalized into a fully qualified URL and returned
        as part of a consolidated list.

        Parameters
        ----------
        nyc_data_content : BeautifulSoup element
            The parsed HTML container (injected by the `access_nyc_data` decorator)
            that holds the TLC documentation and metadata links.

        Returns
        -------
        list of str
            A list of fully qualified URLs pointing to all discovered metadata,
            lookup tables, and reference documentation. Returns an empty list
            if extraction fails or if the section is unavailable.

        Notes
        -----
        - Errors are logged and safely handled to avoid pipeline interruption.
        - Only the first two <ul> elements are parsed, as these consistently contain
        downloadable resources on the TLC website.
    """
    
    file_urls = []
    
    try:
        
        for idx in range(value):
            nyc_file_links_parent_tag = nyc_data_content.find_all('ul')[idx]
            
            nyc_file_url_list = [link for link in nyc_file_links_parent_tag.find_all('li')]
            
            for file_url in nyc_file_url_list:
                
                file_url = file_url.find('a', href=True).get('href')

                file_urls.append(f"{NYC_BASE_URL}{file_url}" if file_url else None)
                            
        logger.info("Files Extracted Successfully")
        
        return file_urls    

    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while extracting download links: {e}")
        return []
    except Exception as e:
        logger.error(f"An Error Occured : {e}")
        return []
        


result = extract_nyc_meta_lookup_data()
print(result)