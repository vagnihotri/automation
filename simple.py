from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

account_id = "1543310976"
base_url = "https://eu1.dashboard.clevertap.com/W67-774-7Z5Z/account/internal/access.html?tempAccountId="
url = base_url + account_id

# declare and initialize driver variable
driver=webdriver.Chrome(executable_path="/Users/vijay.agnihotri/Documents/python/chromedriver")
# browser should be loaded in maximized window
driver.maximize_window()
# driver should wait implicitly for a given duration, for the element under consideration to load.
# to enforce this setting we will use builtin implicitly_wait() function of our 'driver' object.
# to load a given URL in browser window
driver.get(url)
#WebDriverWait(driver,120).until(driver.title.__contains__('Today'))
#while driver.title.__contains__('Today') >= 0:
  #  pass
#driver.save_screenshot("today.png")
# to close the browser
#driver.close()

try:
    element = WebDriverWait(driver, 120).until(
        EC.title_contains('Access')
    )
    ddelement= Select(driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[6]/div[2]/div[2]/div/select'))
    ddelement.select_by_visible_text('CS Troubleshoot')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[3]/div/div/div[6]/div[2]/div[3]/div/p[2]/label'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[3]/div/div/div[6]/div[2]/input'))).click()
    
    element = WebDriverWait(driver, 120).until(
        EC.title_contains('Today')
    )
    fpUrl = driver.current_url.replace("dashboards/daily/today","find-people.html")
    driver.get(fpUrl)
    element = WebDriverWait(driver, 120).until(
        EC.title_contains('Find People')
    )
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[3]/div/div/div[5]/div[1]/div[2]/input'))).click()
    #total_profiles = WebDriverWait(driver, 10).until(EC.element_to_be_selected((By.XPATH, '/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[1]/div[2]'))).text
    time.sleep(5)
    total_profiles = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[1]/div[2]').text
    print("Size of all users segment: " + total_profiles)
    web_push_no = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[2]/div/div[1]/div[2]').text
    web_push_perc = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[2]/div/div[1]/div[3]').text
    print("Web Push reachable profiles: " + web_push_no + "(" + web_push_perc + ")")

    mobile_push_no = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[2]/div/div[2]/div[2]').text
    mobile_push_perc = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[2]/div/div[2]/div[3]').text
    print("Mobile Push reachable profiles: " + mobile_push_no + "(" + mobile_push_perc + ")")

    sms_push_no = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[2]/div/div[3]/div[2]').text
    sms_push_perc = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[2]/div/div[3]/div[3]').text
    print("SMS reachable profiles: " + sms_push_no + "(" + sms_push_perc + ")")

    email_push_no = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[2]/div/div[4]/div[2]').text
    email_push_perc = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[2]/div/div[4]/div[3]').text
    print("Email reachable profiles: " + email_push_no + "(" + email_push_perc + ")")

    wa_push_no = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[2]/div/div[5]/div[2]').text
    wa_push_perc = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[2]/div/div[5]/div[3]').text
    print("WhatsApp reachable profiles: " + wa_push_no + "(" + wa_push_perc + ")")

    aud_push_no = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[2]/div/div[6]/div[2]').text
    aud_push_perc = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[2]/div/div[6]/div[3]').text
    print("Audiences reachable profiles: " + aud_push_no + "(" + aud_push_perc + ")")
finally:
    driver.quit()


# def save_screenshot(driver: webdriver.Chrome, path: str) -> None:
#     # Ref: https://stackoverflow.com/a/52572919/
#     original_size = driver.get_window_size()
#     required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
#     required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
#     driver.set_window_size(required_width, required_height)
#     driver.save_screenshot(path)  # has scrollbar
#     driver.find_element_by_tag_name('body').screenshot(path)  # avoids scrollbar
#     driver.set_window_size(original_size['width'], original_size['height'])