from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

    submit_root = wait_for_element(root, "cib-icon-button[description='Submit']")
    submit_root = expand_shadow_element(driver, submit_root)

    submit_button = wait_for_element_clickable(submit_root, "button")
    submit_button.click()

    while is_ai_responding(driver):
        sleep(1)

from selenium.common.exceptions import NoSuchElementException

'''def get_cib_text_message_elements(driver):
    css = ["cib-serp.cib-serp-main", "cib-conversation[id='cib-conversation-main']"]
    root = traverse_shadow_roots_css(driver, css)

    chat_turns = root.find_elements(By.CSS_SELECTOR,"cib-chat-turn")
    elements = []

    for chat_turn in chat_turns:
        root = expand_shadow_element(driver, chat_turn)
        
        try:
            css = ["cib-message-group.response-message-group", "cib-message[type='text']"]
            root = traverse_shadow_roots_css(root, css)

            elements.append(root)

        except NoSuchElementException:
            continue
    
    return elements'''

def get_cib_text_message_elements(driver):
    '''host_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "cib-serp.cib-serp-main")))
    shadow_root1 = expand_shadow_element(driver, host_element)

    conversation = wait_for_element(shadow_root1, "cib-conversation[id='cib-conversation-main']")
    shadow_root2 = expand_shadow_element(driver, conversation)'''

    css = ["cib-serp.cib-serp-main", "cib-conversation[id='cib-conversation-main']"]
    root = traverse_shadow_roots_css(driver, css)

    chat_turns = root.find_elements(By.CSS_SELECTOR,"cib-chat-turn")
    elements = []

    for chat_turn in chat_turns:
        shadow_root3 = expand_shadow_element(driver, chat_turn)
        
        try:
            host_element = shadow_root3.find_element(By.CSS_SELECTOR,"cib-message-group.response-message-group")
            shadow_root4 = expand_shadow_element(driver, host_element)
    
            '''host_element = shadow_root4.find_element(By.CSS_SELECTOR,"cib-message[type='text']")
            shadow_root5 = expand_shadow_element(driver, host_element)

            elements.append(shadow_root5)'''

            host_element = shadow_root4.find_elements(By.CSS_SELECTOR,"cib-message[type='text']")
            for h in host_element:
                shadow = expand_shadow_element(driver, h)
                elements.append(shadow)
            #shadow_root5 = expand_shadow_element(driver, host_element[0])

            #elements.append(shadow_root5)

            '''for root in host_element:
                shadow_root5 = expand_shadow_element(driver, root)
                elements.append(shadow_root5)'''

        except NoSuchElementException:
            continue
    
    return elements

def get_ai_responses(driver):
    messages = []

    for msg_element in get_cib_text_message_elements(driver):
        # Confirm privacy statement
        try:
            root = msg_element.find_element(By.CSS_SELECTOR,"cib-muid-consent")
            root = expand_shadow_element(driver, resp)
            confirm_button = resp.find_element(By.CSS_SELECTOR,"button")
            confirm_button.click()
        except:
            pass

        try:
            resp = msg_element.find_element(By.CSS_SELECTOR,"div.ac-textBlock")
            messages.append(resp.get_attribute('innerHTML'))
        except:
            print("Element not found, skipping.")
            pass

    return messages

def prompts_left(driver):
    responses = get_cib_text_message_elements(driver)

    # Loop through the responses in reverse order.
    for response in reversed(responses):
        try:
            root = traverse_shadow_roots_css(response, ["cib-turn-counter"])
            spans = root.find_elements(By.CSS_SELECTOR, "span")

            if spans:  # Check if spans is not empty
                first_span = spans[0]
                last_span = spans[-1]

                prompt_num = int(first_span.text)
                max_num_prompts = int(last_span.text)

                return max_num_prompts - prompt_num
        except NoSuchElementException:
            continue
    
    # Return None if no 'cib-turn-counter' was found in any response.
    return None

def enter_text_into_prompt(driver, text):
    #confirm_privacy_statement()

    textarea = get_prompt_textarea(driver)
    
    # Initialize WebDriverWait instance.
    wait = WebDriverWait(textarea, 10)
    
    # Wait for the textarea to be interactable and then retrieve it.
    textarea = wait.until(EC.element_to_be_clickable(textarea))
    
    # Now enter your text into the textarea.
    textarea.send_keys(text)

import os

def upload_image(driver, local_file_path):
    abosolute_file_path = os.path.abspath(local_file_path)

    root = traverse_shadow_roots_actionbar(driver)

    img_input = wait_for_element(root, "input.fileinput[type=file][accept*='image/jpeg']")
    img_input.send_keys(abosolute_file_path)

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