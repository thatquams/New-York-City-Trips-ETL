import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import logging

# configure logging format output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# load environment variables from .env file
load_dotenv()

NYC_BASE_URL = os.getenv("NYC_BASE_URL")
NYC_DATA_EXT = os.getenv("NYC_DATA_EXT")
        
def access_nyc_data(function):
    """
        Decorator that fetches a NYC data page and provides the target HTML element
        to the decorated function.

        The decorated function should accept the BeautifulSoup element (or `None`)
        as its first positional argument, followed by other arguments, if necessary.

        Example:
            @access_nyc_data
            def parse_nyc_data(access_data, other_arg):
                if access_data is None:
                    return None
                # parse and return something

        Args:
            function: The function to wrap. The wrapper will call `function(access_data, *args, **kwargs)`.

        Returns:
            A wrapper function that returns the decorated function's return value,
            or `None` if the page couldn't be fetched or the expected element is missing.

        Notes:
            - This decorator logs attempts and failures.
            - Uses a 10-second request timeout to avoid hanging indefinitely.
    """
    
    def access_nyc_wrapper(*args, **kwargs):
        
 
        NYC_PAGE_URL = f"{NYC_BASE_URL}{NYC_DATA_EXT}"
        logger.info(f"Accessing NYC data page at: {NYC_PAGE_URL}")
        
        try:
            response = requests.get(NYC_PAGE_URL, timeout=10)
 
            if response.status_code == 200:
                nyc_page_content = BeautifulSoup(response.content, 'html.parser')
                
                logger.info("Successfully accessed the NYC data page.")
                
                access_data = nyc_page_content.find('div', class_='span6 about-description')
                
                if access_data is None:
                    logger.warning("Expected content not found in the page.")
                    return None
                
                return function(access_data, *args, **kwargs)
            
            else:
                logger.error(f"Failed to load page. Status code: {response.status_code}")
                return None
            
                                
        except requests.RequestException as e:
            logger.error(f"An error occurred while trying to access {NYC_PAGE_URL}: {e}")
        
        finally:
            logger.info("Finished attempting to access NYC data page.")
            
    return access_nyc_wrapper