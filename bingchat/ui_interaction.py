import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from time import sleep

from .util import *

def traverse_shadow_roots_css(driver, css_list):
    root = driver
    for css in css_list:
        root = wait_for_element(root, css)
        root = expand_shadow_element(driver, root)
    return root

def traverse_shadow_roots_actionbar(driver):
    css = ["cib-serp.cib-serp-main", "cib-action-bar"]
    return traverse_shadow_roots_css(driver, css)

def clear_prompts(driver):
    root = traverse_shadow_roots_actionbar(driver)

    new_topic_button = wait_for_element_clickable(root, "button.button-compose")
    new_topic_button.click()

def get_prompt_textarea(driver):
    root = traverse_shadow_roots_actionbar(driver)

    host_element = wait_for_element(root, "cib-text-input")
    root = expand_shadow_element(driver, host_element)

    return wait_for_element(root, "textarea")

def is_ai_responding(driver):
    root = traverse_shadow_roots_actionbar(driver)

    root = wait_for_element(root, "cib-typing-indicator")
    root = expand_shadow_element(driver, root)

    stop_responding_button = wait_for_element(root, "button")
    
    # return False if button is disabled or True otherwise
    return stop_responding_button.is_enabled()

def submit_prompt(driver):
    root = traverse_shadow_roots_actionbar(driver)

    submit_button = wait_for_element(root, "div > div.main-container > div > div.bottom-controls > div.bottom-right-controls > div.control.submit > button")
    submit_button.click()

    while is_ai_responding(driver):
        sleep(10/1000)

def get_cib_text_message_elements(driver):
    css = ["cib-serp.cib-serp-main", "cib-conversation[id='cib-conversation-main']"]
    root = traverse_shadow_roots_css(driver, css)

    chat_turns = root.find_elements(By.CSS_SELECTOR,"cib-chat-turn")
    elements = []

    for chat_turn in chat_turns:
        shadow_root3 = expand_shadow_element(driver, chat_turn)
        
        try:
            host_element = shadow_root3.find_element(By.CSS_SELECTOR,"cib-message-group.response-message-group")
            shadow_root4 = expand_shadow_element(driver, host_element)

            host_element = shadow_root4.find_elements(By.CSS_SELECTOR,"cib-message[type='text']")
            for h in host_element:
                shadow = expand_shadow_element(driver, h)
                elements.append(shadow)

        except NoSuchElementException:
            continue
    
    return elements

def get_ai_responses(driver):
    messages = []

    for msg_element in get_cib_text_message_elements(driver):
        # Confirm privacy statement
        try:
            root = msg_element.find_element(By.CSS_SELECTOR,"cib-muid-consent")
            root = expand_shadow_element(driver, root)
            confirm_button = root.find_element(By.CSS_SELECTOR,"button")
            confirm_button.click()
        except (NoSuchElementException, TimeoutException):
            pass

        try:
            resp = msg_element.find_element(By.CSS_SELECTOR,"div.ac-textBlock")
            messages.append(resp.get_attribute('innerHTML'))
        except (NoSuchElementException, TimeoutException, WebDriverException):
            pass

    return messages

def prompts_left(driver):
    responses = get_cib_text_message_elements(driver)

    for response in reversed(responses):
        try:
            root = traverse_shadow_roots_css(response, ["cib-turn-counter"])
            spans = root.find_elements(By.CSS_SELECTOR, "span")

            if spans:
                first_span = spans[0]
                last_span = spans[-1]

                prompt_num = int(first_span.text)
                max_num_prompts = int(last_span.text)

                return max_num_prompts - prompt_num
        except NoSuchElementException:
            continue
    
    return None

def enter_text_into_prompt(driver, text):
    textarea = get_prompt_textarea(driver)
    
    wait = WebDriverWait(textarea, 10)
    textarea = wait.until(EC.element_to_be_clickable(textarea))
    
    textarea.send_keys(text)

def upload_image(driver, local_file_path):
    absolute_file_path = os.path.abspath(local_file_path)

    root = traverse_shadow_roots_actionbar(driver)

    img_input = wait_for_element(root, "input.fileinput[type=file][accept*='image/jpeg']")
    img_input.send_keys(absolute_file_path)

    # Wait for upload to complete
    sleep(5)

def get_tone_button_container(driver):
    css = ["cib-serp.cib-serp-main", "cib-conversation[id='cib-conversation-main']", "cib-welcome-container[chat-type='consumer']", "cib-tone-selector"]
    root = traverse_shadow_roots_css(driver, css)
    return root

def click_tone_creative(driver):
    container = get_tone_button_container(driver)

    button = wait_for_element_clickable(container, "button.tone-creative")
    driver.execute_script("arguments[0].click();", button)

def click_tone_balanced(driver):
    container = get_tone_button_container(driver)

    button = wait_for_element_clickable(container, "button.tone-balanced")
    driver.execute_script("arguments[0].click();", button)

def click_tone_precise(driver):
    container = get_tone_button_container(driver)

    button = wait_for_element_clickable(container, "button.tone-creative")
    driver.execute_script("arguments[0].click();", button)
