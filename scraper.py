from selenium import webdriver
import time
import pandas as pd




from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(options=chrome_options)


def read_csv_queries(file_path):
    df = pd.read_csv(file_path)
    return df['query'].tolist()

def search_and_download(driver, query):
    # Navigate to Thingiverse homepage
    driver.get("https://www.thingiverse.com/")
    
    # Input the search query and submit
    search_box = driver.find_element_by_css_selector(".SearchInput__searchInput--HPa9Q")
    search_box.send_keys(query)
    search_box.submit()

    # Wait for search results to load
    time.sleep(5)
    
    index = 0
    while True:
        try:
            # Get a list of models from search results
            model_elements = driver.find_elements_by_css_selector(".ThingCardHeader__cardNameWrapper--VgmUP")
            if index >= len(model_elements):
                break
            
            model_element = model_elements[index]
            model_element.click()  # Click on the model to navigate to its page
            time.sleep(5)

            # Click the "Download All Files" button
            download_button = driver.find_element_by_css_selector(".Button__button--xv8c4.Button__primary--grPsm.Button__left--Zsp9y.Button__md--hfp1W.Button__icon--UCU2X")
            download_button.click()

            # Wait for download to complete and then navigate back to search results
            time.sleep(10)
            driver.back()
            time.sleep(5)

            index += 1
        except Exception as e:
            print(f"Error processing model at index {index}: {e}")
            break

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
