from selenium import webdriver

from .util import wait_for_element_clickable
from .ui_interaction import *

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def open_bing_and_click_chat(driver):
    driver.get("https://www.bing.com/")
    chat_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[.//*[contains(text(), 'Chat')]]")))
    chat_button.click()

class BingChat:
    def __init__(self):
        #self.driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=self.options)
        options = webdriver.EdgeOptions()
        options.use_chromium = True
        options.binary_location = '/usr/bin/microsoft-edge-stable'

        self.driver = webdriver.Edge()
        open_bing_and_click_chat(self.driver)

    def set_tone_creative(self):
        click_tone_creative(self.driver)

    def set_tone_balanced(self):
        click_tone_balanced(self.driver)

    def set_tone_precise(self):
        click_tone_precise(self.driver)

    def set_prompt(self, text):
        prompts_remaining = self.prompts_left()
        if prompts_remaining == 0:
            raise Exception("No prompts remaining.")
            
        enter_text_into_prompt(self.driver, text)

    def upload_image(self, path):
        prompts_remaining = self.prompts_left()
        if prompts_remaining == 0:
            raise Exception("No prompts remaining.")
            
        upload_image(self.driver, path)

    def clear_prompts(self):
        clear_prompts(self.driver)

    def submit(self):
        submit_prompt(self.driver)
        response = get_ai_responses(self.driver)
        if response:
            return response[-1]
        else:
            return None

    def get_all_responses(self):
        return get_ai_responses(self.driver)

    def prompts_left(self):
        return prompts_left(self.driver)