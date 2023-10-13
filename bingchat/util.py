from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

def expand_shadow_element(driver, element):
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
    return shadow_root

def wait_for_element(driver, css_selector, timeout=10):
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

def wait_for_element_visible(driver, css_selector, timeout=10):
    wait = WebDriverWait(driver, timeout) 
    return wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))

def wait_for_element_clickable(driver, css_selector, timeout=10):
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
