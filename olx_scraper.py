import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import traceback
import csv
import logging
from datetime import datetime
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_driver():
    """Setup and return the undetected Chrome driver"""
    try:
        options = uc.ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-notifications")
        return uc.Chrome(options=options)
    except Exception as e:
        logger.error(f"Failed to setup Chrome driver: {str(e)}")
        raise

def load_all_results(driver, wait, max_scrolls=3):
    last_count = 0
    scrolls = 0
    while scrolls < max_scrolls:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        try:
            load_more_btn = driver.find_element(By.CSS_SELECTOR, 'button[data-aut-id="btnLoadMore"]')
            if load_more_btn.is_displayed():
                driver.execute_script("arguments[0].scrollIntoView();", load_more_btn)
                driver.execute_script("arguments[0].click();", load_more_btn)
                logger.info("Clicked 'Load More' button.")
                time.sleep(5)
        except Exception as e:
            print(e)
            pass
        # Wait for new cards to load
        cards = driver.find_elements(By.CSS_SELECTOR, 'li[data-aut-id^="itemBox"]')
        if len(cards) == last_count:
            logger.info("No more new cards loaded. Stopping scroll.")
            break
        last_count = len(cards)
        scrolls += 1
        logger.info(f"Scroll {scrolls}: {last_count} cards loaded.")
    logger.info(f"Total cards loaded: {last_count}")

def scrape_olx_car_covers():
    """Main function to scrape car covers from OLX"""
    driver = None
    try:
        driver = setup_driver()
        logger.info("Starting OLX car cover scraping...")
        
        url = "https://www.olx.in/items/q-car-cover"
        driver.get(url)
        
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li[data-aut-id^="itemBox"]')))
        
        # Load all results by scrolling and clicking 'Load More'
        load_all_results(driver, wait)
        
        cards = driver.find_elements(By.CSS_SELECTOR, 'li[data-aut-id^="itemBox"]')
        logger.info(f"Found {len(cards)} cards after loading all results")
        
        results = []
        for card in cards: 
            price,location,title = ["N/A",]*3 
            try:
                link = card.find_element(By.TAG_NAME, 'a').get_attribute('href')
                try:
                    img = card.find_element(By.CSS_SELECTOR, 'img._3vnjf').get_attribute('src')
                except NoSuchElementException:
                    img = ''
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-aut-id="itemPrice"]')))    
                try:
                 price = card.find_element(By.CSS_SELECTOR, 'span[data-aut-id="itemPrice"]').text.strip()
                 title = card.find_element(By.CSS_SELECTOR, 'span[data-aut-id="itemTitle"]').text.strip()
                 location = card.find_element(By.CSS_SELECTOR, 'span[data-aut-id="item-location"]').text.strip()
                except:
                    pass
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-aut-id="itemTitle"]')))    
                try:
                    date = card.find_element(By.CSS_SELECTOR, 'span._2jcGx > span').text.strip()
                except NoSuchElementException:
                    date = ''
                results.append([title, price, location, date, link, img])
                logger.debug(f"Scraped product: {title}")
                
            except Exception as e:
                logger.warning(f"Failed to scrape a card: {str(e)}")
                continue
        
        filename = f"olx_car_cover.csv"
        
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Title", "Price", "Location", "Date", "Link", "Image"])
            writer.writerows(results)
        
        logger.info(f"✅ Results saved to {filename}")
        return filename
        
    except TimeoutException:
        logger.error("Timeout while waiting for page to load")
        raise
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise
    finally:
        if driver:
            driver.quit()
            logger.info("Browser closed")

if __name__ == "__main__":
    try:
        output_file = scrape_olx_car_covers()
        print(f"Scraping completed successfully! Results saved to: {output_file}")
    except Exception as e:
        print(f"Scraping failed: {str(e)}")
