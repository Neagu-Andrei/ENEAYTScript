from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import logging
import socket
import time

logger = logging.getLogger(__name__)


class DriverController:
    ytLink = "https://www.youtube.com/"
    adButtonXPath = "//*[@id='skip-button:6']/span/button"
    # adButtonXPath = "/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div/div/div/ytd-player/div/div/div[4]/div/div[3]/div/div[2]/span/button"
    # adButtonXPath = "#skip-button\:6 > span > button"

    # Standard XPath to the agreeButton returns //*[@id="button"] and can't differencate between the other buttons
    agreeButtonXPath = "//*[@aria-label='Agree to the use of cookies and other data for the purposes described']"

    # Opening the Chrome Driver and maximizing window to the screen size
    def __init__(self, seconds):
        self.seconds = seconds
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def connection(self):
        try:
            appsocket = socket.socket()
            appsocket.connect(("8.8.8.8", 53))
            return True
        except socket.error:
            return False

    # Trying to open YouTube and wait 10 seconds
    # If there was a problem opening the link (e.g. the link was not a valid one) we log the error message and stop
    # the program
    def open_yt(self):
        try:
            if self.connection():
                self.driver.get(self.ytLink)
                self.driver.implicitly_wait(10)
            else:
                self.open_yt()
        except WebDriverException as error:
            logger.critical(error.msg + "\n")
            raise

    # Function that click the Agree Cookies button
    # Logs a warning that we couldn't find it and something may be wrong down the line
    def agree_cookies(self):
        for _ in range(3):
            try:
                if self.connection():
                    element = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, self.agreeButtonXPath)))
                    element.click()
                    break
                else:
                    logger.error("Internet connection failed. Couldn't click the agree button\n")
                    continue
            except TimeoutException:
                logger.warning("Couldn't find the agree button")
                break
            except ElementClickInterceptedException:
                logger.error("Couldn't press agree button\n")
                raise

    # Takes 2 arguments:
    #   - numbers selects which video we want to display (e.g for the 3rd video in Recommended, number = 2)
    #   - path is the XPath to all the videos in a given page (defaults to the main page)
    def select_video(self, number=0, path="//*[@id='contents']/ytd-rich-item-renderer"):
        try:
            if self.connection():
                videos = self.driver.find_elements(By.XPATH, path)
                if len(videos) == 0:
                    raise NoSuchElementException
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(videos[number])).click()
            else:
                raise socket.error
        except NoSuchElementException:
            logger.warning("Path to the video might be wrong")
        except TimeoutException:
            logger.critical("Element is not clickable")
            raise
        except IndexError:
            logger.critical("The element you are trying to select is not in the array of elements\n")
            raise
        except socket.error:
            logger.error("Internet connection failed. Couldn't select video\n")
            raise

    # A search using Selenium that finds the search bar, clicks on it, adds the input that we wont
    # and then selects the first video that is recommended.
    def search_for_video(self, name):
        try:
            if self.connection():
                searchbar = WebDriverWait(self.driver, 10).until(
                    (EC.visibility_of_element_located((By.CSS_SELECTOR, "input#search"))))
                searchbar.click()
                searchbar.send_keys(name)
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='search-icon-legacy']"))).click()
                self.select_video(0, "//*[@id='contents']/ytd-video-renderer")
            else:
                raise socket.error
        except socket.error:
            logger.error("Internet connection failed. Couldn't search the name\n")
            raise
        except NoSuchElementException:
            logger.warning("Path to the search bar or search icon might be wrong")

    # A search bar more "reliable" because it looks at the link that is generated when searching
    # Reliability due to the fact that YouTube is less likely to change how links are generated rather than
    # the HTML code for a page
    # def search_for_video(self, name):
    #     if self.connection():
    #         link = "https://www.youtube.com/results?search_query="
    #         wordList = name.split()
    #         link += wordList.pop(0)
    #         for word in wordList:
    #             link += f"+{word}"
    #         self.driver.implicitly_wait(10)
    #         self.driver.get(link)
    #         self.select_video(0, "//*[@id='contents']/ytd-video-renderer")
    #     else:
    #         logger.error("Internet connection failed")
    #         raise

    # Function to determine if a given ad is skippable ad or not and logs the action
    def skip_ad(self):
        try:
            if self.connection():
                element = WebDriverWait(self.driver, 20).until(
                    EC.visibility_of_element_located((By.XPATH, self.adButtonXPath)))
                element.click()
                logger.info("Ad skipped")
            else:
                raise socket.error
        except TimeoutException:
            logger.info("No skippable ad displayed")
        except socket.error:
            logger.error("Internet connection failed. Couldn't skip ad\n")
            raise

    def time_connected(self):
        start_time = time.time()
        while time.time() - start_time < self.seconds:
            if not self.connection():
                logger.error("Internet connection failed")
                break
            else:
                continue
        logger.info("Connection was successful")

    def run(self):
        logger.info("Incepe executarea deschiderea yt")
        self.open_yt()
        self.agree_cookies()
        self.search_for_video("music")
        self.skip_ad()
        logger.info("S-a executat deschiderea yt")

    # Function to stop the driver when the process is ended
    def stop(self):
        self.driver.quit()
