import re
from botasaurus.browser import browser, Driver, Wait
from botasaurus.soupify import soupify
import time

@browser(cache=False)
def scrape_heading_task(driver: Driver, data):
    # Visit the Reed Website
    driver.google_get("https://www.reed.co.uk/jobs/contract-devops-outside-ir35-jobs-in-united-kingdom")

    # Accept cookies if prompted
    accept_btn = driver.select('#onetrust-accept-btn-handler', wait=Wait.SHORT)
    if accept_btn:
        accept_btn.click()
        time.sleep(5)

    # Gets the Main Element
    parent_main = driver.select("main.search-results_hide__9cTQ5")
    if parent_main:

        # Make a soup of main element
        soup = soupify(parent_main)

        # Extract Job data 
        buttons = parent_main.select_all('button[data-qa="job-title-btn-wrapper"]')
        for i in buttons:
            i.click()
            time.sleep(5)
        headings = soup.find_all('h2') 
        companies = soup.find_all("a", {"data-page-component":"job_card"}) 
        locations = soup.find_all('li', {'data-qa': 'job-card-location'}) 
        other_options = soup.find_all('ul', {"data-qa": "job-card-options"})
        
        # Iterate over data fields
        # for i in range(len(headings)):
            # description_buttons[i].click()
            # description = soup.find('p',{'data-qa': 'jobDescriptionDetails'}).text
            # job_role = headings[i].text.strip()
            # company = companies[i].text.strip()
            # location = locations[i].text.strip()
            # other_info = other_options[i].text.strip()

            # # Format the "Other info" field
            # formatted_info = format_other_info(other_info)

            # # Print the structured data
            # print(f"Job Role: {job_role}")
            # print(f"Company: {company}")
            # print(f"Location: {location}")
            # # print(f"Job Description: {description}")
            # print(f"Other info: {formatted_info}")
            # print('\n\n')
    else:
        return "No parent object found"


# Function to format "Other info"
def format_other_info(other_info):
    """
    Adds spacing between concatenated fields in the "Other info" text for readability.
    """
    # Add spaces before capitalized words or locations
    formatted_info = re.sub(r"(\d+ per day|negotiable)([A-Z])", r"\1   \2", other_info)
    formatted_info = re.sub(r"([a-z,])([A-Z])", r"\1   \2", formatted_info)
    formatted_info = re.sub(r"(\w)(Contract|full-time|Work from home)", r"\1   \2", formatted_info)
    
    return formatted_info


# Initiate the web scraping task
scrape_heading_task()
