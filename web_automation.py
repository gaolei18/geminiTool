import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    edge_options = EdgeOptions()
    # To prevent detection, we can try to mimic a real user agent
    edge_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59")
    
    try:
        driver = webdriver.Edge(options=edge_options)
        driver.get("https://www.ceair.com")

        wait = WebDriverWait(driver, 30) # Increased wait time to 30 seconds

        # --- Handle Cookie Consent ---
        try:
            # Using a more specific selector for the agree button
            agree_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.pop-box-cookie a.btn-agree")))
            agree_button.click()
            print("Clicked cookie consent button.")
        except Exception as e:
            print(f"Cookie button not found or not clickable, continuing... Reason: {e}")

        # --- Fill Departure and Destination ---
        
        # 1. Click and fill departure city
        departure_input = wait.until(EC.element_to_be_clickable((By.ID, "departureAirport")))
        departure_input.send_keys("上海")
        print("Entered '上海' as departure.")
        time.sleep(1)
        
        # 2. Select the first option from the dropdown
        departure_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ul.airport-list > li:first-child")))
        departure_option.click()
        print("Selected first departure option.")
        time.sleep(1)

        # 3. Click and fill destination city
        destination_input = wait.until(EC.element_to_be_clickable((By.ID, "destinationAirport")))
        destination_input.send_keys("北京")
        print("Entered '北京' as destination.")
        time.sleep(1)

        # 4. Select the first option from the dropdown
        destination_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ul.airport-list > li:first-child")))
        destination_option.click()
        print("Selected first destination option.")
        time.sleep(1)

        # --- Click Search ---
        search_button = wait.until(EC.element_to_be_clickable((By.ID, "search-button")))
        search_button.click()
        print("Clicked the search button.")

        wait.until(EC.title_contains("航班查询"))
        print("Flight results page loaded successfully.")
        
        print("Automation complete. Browser will close in 10 seconds.")
        time.sleep(10)

    except Exception as e:
        print(f"An error occurred during automation: {e}", file=sys.stderr)
    
    finally:
        if 'driver' in locals() and driver:
            driver.quit()
            print("Browser closed.")

if __name__ == "__main__":
    main()