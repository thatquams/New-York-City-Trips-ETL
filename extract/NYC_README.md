# 🗂️ NYC TLC Trip Data Extraction — Project Documentation
📌 Overview

This project automates the extraction of NYC Taxi & Limousine Commission (TLC) Trip Record data from the official NYC website. The page hosting these datasets is fully dynamic—its content is hidden behind expandable FAQ sections, which require JavaScript execution and user interaction before the dataset links can be retrieved.

To handle this, the project combines:

    - Selenium for rendering and interacting with dynamic page elements

    - Requests for lightweight HTTP retrieval after expansion

    - BeautifulSoup (bs4) for efficient HTML parsing

    - A custom decorator to encapsulate all page-access logic

    - Logging for traceability and debugging

This document explains the extraction workflow implemented up to this point.

## 📚 Extraction Workflow Summary
The extraction pipeline consists of four major stages:

    - Environment initialization

    - Dynamic page rendering with Selenium

    - Page content retrieval via requests

    - HTML parsing with BeautifulSoup and data hand-off

Each is documented in detail below.

## ⚙️ 1. Environment Initialization

Before page access begins:

    - Environment variables (NYC_BASE_URL, NYC_DATA_EXT) are loaded from .env.

    - ChromeDriver is automatically installed (if missing) using chromedriver_autoinstaller.

    - Logging is configured for standardized timestamped logs.

    - Headless Chrome is set up to run in a lightweight environment.

This ensures a consistent runtime environment across systems.

## 🧭 2. Dynamic Page Rendering via Selenium

The NYC TLC data page is not static.

Key datasets for each year are contained within collapsible FAQ sections that do not exist in the initial HTML until a user clicks the "Expand All" button.

To render these sections:

A headless Selenium Chrome instance is opened.

Selenium navigates to the combined URL:

    - Selenium waits for the "Expand All" button to appear.

    - The script scrolls into view and clicks it.

    - A delay is added to allow all year sections to expand.

    - The fully rendered HTML is now visible in the DOM.

This step is necessary because the website loads content dynamically, meaning a traditional requests.get() would never show the expanded dataset table.

## 🌐 3. Page Retrieval Using requests (Optimized Fetch)

Once Selenium expands the FAQs, the project retrieves:

    - The current URL (which may change depending on site structure)

    - The fully rendered HTML of the page via requests.get()

Why this hybrid approach?

✔ Selenium renders the dynamic content
✔ Requests fetches HTML faster, with less overhead
✔ It avoids expensive .page_source extraction in Selenium

This method gives you the best of both worlds: dynamic rendering + fast HTML access.

## 🧵 4. HTML Parsing with BeautifulSoup

After successfully fetching the HTML:

The page is wrapped inside a BeautifulSoup parser:

    - BeautifulSoup(response.content, 'html.parser')


The relevant content block is extracted:

    - nyc_page_content.find('div', class_='span6 about-description')


This div contains:

    - Year-grouped trip record tables

    - Download links

    - Metadata such as month names

This extracted block is passed to the downstream parsing function (e.g., trips_record_data_links) through the decorator.

The downstream function can then:

    - Find all tables

    - Loop through year sections

    - Extract <td> cells

    - Retrieve dataset URLs from <a> tags

    - Log progress (year, month, number of links)

This modular design keeps extraction steps clean and reusable.

## 🧩 Decorator Architecture

The heart of the workflow is the custom decorator:

@access_nyc_data

It wraps any parsing function and automatically handles:

    - Browser setup & teardown

    - Page navigation

    - Dynamic HTML expansion

    - Robust error handling

    - Logging of each extraction step

    - Passing the parsed BeautifulSoup element into the decorated function

This approach isolates Selenium complexity from your parsing logic, allowing each extraction script to focus solely on data processing.

## 🧪 Error Handling & Reliability

The workflow includes defensive programming to ensure reliability:

    - Catches requests exceptions

    - Catches Selenium WebDriverException and TimeoutException

    - Catches missing DOM elements (NoSuchElementException)

    - Logs warnings if expected HTML blocks aren’t found

    - Ensures ChromeDriver always closes (via finally)

This prevents hanging processes and ensures clean exit.

## ✨ Current Output

At this stage, the extraction pipeline successfully produces:

    - A complete list of download links for NYC TLC trip record datasets

    - Extracted directly from the fully expanded FAQ tables

    - With corresponding logs for each year and month processed