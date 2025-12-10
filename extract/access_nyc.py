import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    WebDriverException, TimeoutException, NoSuchElementException
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import os
from dotenv import load_dotenv
import logging
import time

# configure logging format output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# install chromedriver if not present, to run the pages that require selenium
chromedriver_autoinstaller.install()

# load environment variables from .env file
load_dotenv()

NYC_BASE_URL = os.getenv("NYC_BASE_URL")
NYC_DATA_EXT = os.getenv("NYC_DATA_EXT")
        
def access_nyc_data(function):
    """
        Decorator that automates access to the NYC TLC trip data page, expands all
        dynamic FAQ sections using Selenium, fetches the fully-rendered HTML, and 
        passes the relevant content block into the decorated function for parsing.

        This decorator:
            • Launches a headless Chrome browser via Selenium
            • Navigates to the NYC Taxi & Limousine Commission data page
            • Clicks the “Expand All” button to reveal hidden year sections
            • Retrieves the fully expanded page content using `requests`
            • Extracts the main data container (`div.span6.about-description`)
            • Passes that container to the decorated function as its first argument

        The decorated function should expect the extracted BeautifulSoup element 
        (or None if unavailable) as its first positional argument. Any additional
        arguments may be supplied normally.

        Example:
            @access_nyc_data
            def parse_tlc_data(content):
                if content is None:
                    return None
                # process data here

        Args:
            function (callable):
                The parsing function that will receive the extracted content.

        Returns:
            callable:
                A wrapper that handles browser automation, error handling, logging,
                and then invokes the decorated function with the processed HTML.

        Notes:
            - Selenium is used because the page requires client-side interaction 
            (click-to-expand) before the relevant HTML becomes available.
            - A 10-second wait ensures the “Expand All” button and dynamic content load.
            - All network, Selenium, and parsing errors are logged for debugging.
            - The browser instance is closed automatically after execution.
    """
    
    def access_nyc_wrapper(*args, **kwargs):
        
 
        NYC_PAGE_URL = f"{NYC_BASE_URL}{NYC_DATA_EXT}"
        logger.info(f"Accessing NYC data page at: {NYC_PAGE_URL}")
        
        try:
            options = Options()
            options.add_argument("--headless")  # Run in headless mode
            options.add_argument("--disable-gpu") 
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
 

            driver = webdriver.Chrome(options=options)
            driver.get(NYC_PAGE_URL)
            
            expand_all_contents = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "faq-expand-all")))
            
            scroll_action = ActionChains(driver)
            scroll_action.move_to_element(expand_all_contents).perform()
            
            time.sleep(2)  # wait for 2 seconds to ensure any dynamic content loads
            
            expand_all_contents.click() # click to expand all contents

            
            current_url = driver.current_url # get the current URL of the page

            
            response = requests.get(current_url, timeout=10)
            
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
            
        except WebDriverException as e:
            logger.error(f"Selenium WebDriver error occurred: {e}")
            
        except TimeoutException as e:   
            logger.error(f"Timeout while trying to load the page: {e}")
            
        except NoSuchElementException as e:
            logger.error(f"Could not find the expected element on the page: {e}")
        
        finally:
            logger.info("Finished attempting to access NYC data page.")
            driver.close()
            driver.quit() # close the browser
            
    return access_nyc_wrapper
