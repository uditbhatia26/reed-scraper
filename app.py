import re
import time
from flask import Flask, jsonify
from botasaurus.browser import browser, Driver, Wait
from botasaurus.soupify import soupify

app = Flask(__name__)

@browser(cache=False)
def scrape_heading_task(driver: Driver, data=None):
    # Visit the Reed Website
    driver.google_get("https://www.reed.co.uk/jobs/contract-devops-outside-ir35-jobs-in-united-kingdom")
    soup = soupify(driver)

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
        headings = soup.find_all('h2')
        companies = soup.find_all("a", {"data-page-component": "job_card"})
        locations = soup.find_all('li', {'data-qa': 'job-card-location'})
        other_options = soup.find_all('ul', {"data-qa": "job-card-options"})

        jobs = []

        # Iterate over data fields
        for i in range(len(headings)):
            job_role = headings[i].text.strip()
            company = companies[i].text.strip()
            location = locations[i].text.strip()
            other_info = other_options[i].text.strip()

            # Format the "Other info" field
            formatted_info = format_other_info(other_info)

            # Append to job list
            jobs.append({
                "Job Role": job_role,
                "Company": company,
                "Location": location,
                "Other Info": formatted_info
            })

        return jobs
    return []

# Function to format "Other info"
def format_other_info(other_info):
    """
    Adds spacing between concatenated fields in the "Other info" text for readability.
    """
    formatted_info = re.sub(r"(\d+ per day|negotiable)([A-Z])", r"\1   \2", other_info)
    formatted_info = re.sub(r"([a-z,])([A-Z])", r"\1   \2", formatted_info)
    formatted_info = re.sub(r"(\w)(Contract|full-time|Work from home)", r"\1   \2", formatted_info)

    return formatted_info

# Flask endpoint
@app.route('/scrape', methods=['GET'])
def scrape():
    try:
        results = scrape_heading_task()
        return jsonify({"status": "success", "data": results}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
