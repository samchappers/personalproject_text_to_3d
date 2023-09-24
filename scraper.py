from selenium import webdriver
import time
import pandas as pd

def read_csv_queries(file_path):
    df = pd.read_csv(file_path)
    return df['query'].tolist()

def search_and_download(driver, query):
    # Navigate to Thingiverse homepage
    driver.get("https://www.thingiverse.com/")

    # Input the search query and submit
    # Note: The selectors here are placeholders; you'll need to inspect the webpage to get the correct ones.
    search_box = driver.find_element_by_css_selector(".search-input-class")
    search_box.send_keys(query)
    search_box.submit()

    # Wait for search results to load
    time.sleep(5)

    # Get a list of models from search results
    models = driver.find_elements_by_css_selector(".model-link-class")

    for model in models:
        # Click on the model to navigate to its page
        model.click()
        time.sleep(5)

        # Click the "Download All Files" button
        download_button = driver.find_element_by_css_selector(".download-all-files-button-class")
        download_button.click()

        # Wait for download to complete and then navigate back to search results
        time.sleep(10)
        driver.back()
        time.sleep(5)

def main():
    # Set up the Selenium driver
    driver = webdriver.Chrome()

    # Read search queries
    queries = read_csv_queries('queries.csv')

    # For each query, perform the search and download files
    for query in queries:
        search_and_download(driver, query)

    driver.quit()

if __name__ == '__main__':
    main()
