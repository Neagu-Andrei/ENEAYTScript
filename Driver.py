from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import threading


class DriverController:
    ytLink = "https://www.youtube.com/"
    agreeButtonXPath = "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[2]/div[2]/div[""5]/div[2]/ytd-button-renderer[2]/a/tp-yt-paper-button/yt-formatted-string"
    adButtonXPath = "//*[@id='skip-button:x']/span/button"

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def open_yt(self):
        try:
            self.driver.get(self.ytLink)
            self.driver.implicitly_wait(10)
        except WebDriverException as error:
            print(error.msg)

    def agree_cookies(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.agreeButtonXPath))).click()

    def select_video(self, path, number):
        videos = self.driver.find_elements(By.XPATH, path)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(videos[number])).click()
        # de facut butonul de skip in cazul in care reclama este prea lunga
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='skip-button:x']/span/button"))).click()
        skipButton = self.driver.find_element(By.XPATH, self.adButtonXPath)
        self.skip_ad(skipButton)

    def search_for_video(self, name):
        searchbar = WebDriverWait(self.driver, 10).until(
            (EC.visibility_of_element_located((By.CSS_SELECTOR, "input#search"))))
        searchbar.click()
        searchbar.send_keys(name)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='search-icon-legacy']"))).click()
        # self.driver.implicitly_wait(10)
        self.select_video("//*[@id='contents']/ytd-video-renderer[1]", 0)

    def skip_ad(self, skipButton):
        threading.Timer(5, self.skip_ad).start()
        if skipButton.is_enabled() or skipButton.is_displayed():
            skipButton.click()

# //*[@id='content']/ytd-rich-grid-media -> main page
