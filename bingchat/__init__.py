import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .util import wait_for_element_clickable
from .ui_interaction import *

class PromptUnavailableException(Exception):
    def __init__(self):
        super().__init__("No prompts remaining.")

def open_bing_and_click_chat(driver):
    driver.get("https://www.bing.com/")
    chat_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[.//*[contains(text(), 'Chat')]]")))
    chat_button.click()

class BingChat:
    def __init__(self, headless=False):
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument('--headless')

        self.driver = webdriver.Edge(options=options)
        open_bing_and_click_chat(self.driver)

    def set_tone_creative(self):
        try:
            click_tone_creative(self.driver)
        except Exception as e:
            print(f'Error setting creative tone: {str(e)}')

    def set_tone_balanced(self):
        try:
            click_tone_balanced(self.driver)
        except Exception as e:
            print(f'Error setting balanced tone: {str(e)}')

    def set_tone_precise(self):
        try:
            click_tone_precise(self.driver)
        except Exception as e:
            print(f'Error setting precise tone: {str(e)}')

    def set_prompt(self, text):
        prompts_remaining = self.prompts_left()
        if prompts_remaining == 0:
            raise PromptUnavailableException()
        try:
            enter_text_into_prompt(self.driver, text)
        except Exception as e:
            print(f'Error setting prompt: {str(e)}')

    def upload_image(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError("The specified file path does not exist.")
        prompts_remaining = self.prompts_left()
        if prompts_remaining == 0:
            raise PromptUnavailableException()
        try:
            upload_image(self.driver, path)
        except Exception as e:
            print(f'Error uploading image: {str(e)}')

    def clear_prompts(self):
        try:
            clear_prompts(self.driver)
        except Exception as e:
            print(f'Error clearing prompts: {str(e)}')

    def submit(self):
        try:
            submit_prompt(self.driver)
            response = get_ai_responses(self.driver)
            if response:
                return response[-1]
            else:
                return None
        except Exception as e:
            print(f'Error submitting the prompt: {str(e)}')

    def get_all_responses(self):
        try:
            return get_ai_responses(self.driver)
        except Exception as e:
            print(f'Error getting all responses: {str(e)}')

    def prompts_left(self):
        try:
            return prompts_left(self.driver)
        except Exception as e:
            print(f'Error getting number of prompts left: {str(e)}')
