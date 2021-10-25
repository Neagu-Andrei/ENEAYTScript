from selenium.common.exceptions import WebDriverException,NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class DriverController:
    ytLink = "https://www.youtube.com/"
    agreeButtonXPath = "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[2]/div[2]/div[""5]/div[2]/ytd-button-renderer[2]/a/tp-yt-paper-button/yt-formatted-string"
    adButtonXPath = "/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div/div/div/ytd-player/div/div/div[17]/div/div[3]/div/div[2]/span/button"

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

    def search_for_video(self, name):
        searchbar = WebDriverWait(self.driver, 10).until(
            (EC.visibility_of_element_located((By.CSS_SELECTOR, "input#search"))))
        searchbar.click()
        searchbar.send_keys(name)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='search-icon-legacy']"))).click()
        self.select_video("//*[@id='contents']/ytd-video-renderer[1]", 0)

    def skip_ad(self):
        self.driver.implicitly_wait(10)
        try:
            self.driver.find_element(By.XPATH, self.adButtonXPath).click()
        except NoSuchElementException:
            print("No skippable ad displayed")

    def stop(self):
        self.driver.quit()
