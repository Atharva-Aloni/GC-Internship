import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time


class GetSearchResults:
   
    
    def __init__(self, query: str, n_scrolls: int = 5, headless: bool = True) -> None:
       
        self.query = query
        self.n_scrolls = n_scrolls
        self.title = []
        self.description = []
        self.url = []

        # Initialize Chrome WebDriver with optional headless mode
        options = Options()
        if headless:
            options.add_argument("--headless")
        self.driver = Chrome(options=options)
        
        print("[INFO]: Starting connection...")
        self.driver.get(f"https://www.google.com/search?q={query}")
        print("[INFO]: Connection established.")

        self._scroll_and_extract()

    def _scroll_and_extract(self):
        """Scroll the page and extract search results."""
        try:
            for _ in range(self.n_scrolls):
                self._scroll_page()
            self._extract_info()
        finally:
            self.driver.quit()
            print("[INFO]: Connection closed.")

    def _scroll_page(self):
        """Scrolls the page to load more results."""
        body = self.driver.find_element(By.TAG_NAME, value="body")
        body.send_keys(Keys.END)
        time.sleep(2)  # Adjustable based on internet speed

    def _extract_info(self):
        """Extracts search result titles, descriptions, and URLs."""
        print("[INFO]: Extracting information...")
        try:
            results_container = self.driver.find_element(By.ID, value="main")
            result_elements = results_container.find_elements(By.CLASS_NAME, value="MjjYud")

            for element in result_elements:
                try:
                    heading = element.find_element(By.CSS_SELECTOR, value="h3.LC20lb.MBeuO.DKV0Md")
                    description = element.find_element(By.CSS_SELECTOR, value="div.VwiC3b.yXK7lf.lyLwlc.yDYNvb.W8l4ac.lEBKkf")
                    link = element.find_element(By.CSS_SELECTOR, value="a").get_attribute("href")

                    self.title.append(heading.text)
                    self.description.append(description.text)
                    self.url.append(link)
                except Exception as e:
                    print(f"[WARNING]: Failed to extract a result. Error: {e}")
        except Exception as e:
            print(f"[ERROR]: Failed to locate results. Error: {e}")
        print("[INFO]: Information extraction completed.")

    def to_csv(self, file_path: str = "./search_results.csv"):
        """
        Saves the extracted data to a CSV file.
        
        Args:
            file_path (str): Path to save the CSV file (default './search_results.csv').
        """
        data = {
            "Title": self.title,
            "Description": self.description,
            "URL": self.url,
        }
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        print(f"[INFO]: CSV file created at {file_path}")


if __name__ == "__main__":
    query = "Internshala"
    obj = GetSearchResults(query=query, n_scrolls=5, headless=True)
    obj.to_csv("./search_results.csv")
