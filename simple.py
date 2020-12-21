from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import sys
import os

regions = ["eu","in","sg","us","sk"]

account_id = input("Enter 12 Character Account ID: ")
if len(account_id) != 12 or account_id[3] != '-' or account_id[7] != '-' :
    sys.exit("Invalid Account Id Entered")
region =  input("Enter Region (eu/in/sg/us/sk): ")
if region not in regions :
    sys.exit("Invalid Region Entered")
if region == "eu":
    demo_acc_id = "ZWW-WWW-WWWZ"
elif region == "in":
    demo_acc_id = "ZWW-WWW-WW4Z"
else:
    demo_acc_id = input("Enter 12 Character Bearded Robot Account ID for " + region + " region: ")
    if len(demo_acc_id) != 12 or demo_acc_id[3] != '-' or demo_acc_id[7] != '-' :
        sys.exit("Invalid Bearded Robot Account Id Entered")
region = region + "1"
base_url = "https://" + region + ".dashboard.clevertap.com/"+ demo_acc_id +"/account/internal/access.html?tempAccountId="
url = base_url + account_id

path = os.getcwd() + "/chromedriver"
chrome_options = Options()
chrome_options.add_argument("user-data-dir=~/Library/Application\ Support/Google/Chrome")
driver=webdriver.Chrome(executable_path=path, options=chrome_options)

driver.maximize_window()

driver.get(url)

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
    fpUrl = driver.current_url.replace("dashboards/daily/today","find-people.html?showDebugEvents=true")
    driver.get(fpUrl)
    element = WebDriverWait(driver, 120).until(
        EC.title_contains('Find People')
    )
    datatable = {}
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[3]/div/div/div[5]/div[1]/div[2]/input'))).click()
    time.sleep(10)
    total_profiles = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[1]/div[2]').text
    print("Size of all users segment: " + total_profiles)
    datatable["Total Profiles"] = total_profiles
    web_push_no = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[2]/div/div[1]/div[2]').text
    web_push_perc = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[2]/div/div[1]/div[3]').text
    print("Web Push reachable profiles: " + web_push_no + "(" + web_push_perc + ")")
    datatable["Web Push Reachable Profiles"] = web_push_no

    mobile_push_no = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[2]/div/div[2]/div[2]').text
    mobile_push_perc = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[2]/div/div[2]/div[3]').text
    print("Mobile Push reachable profiles: " + mobile_push_no + "(" + mobile_push_perc + ")")
    datatable["Mobile Push Reachable Profiles"] = mobile_push_no

    sms_push_no = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[2]/div/div[3]/div[2]').text
    sms_push_perc = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[2]/div/div[3]/div[3]').text
    print("SMS reachable profiles: " + sms_push_no + "(" + sms_push_perc + ")")
    datatable["SMS Reachable Profiles"] = sms_push_no

    email_push_no = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[2]/div/div[4]/div[2]').text
    email_push_perc = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[2]/div/div[4]/div[3]').text
    print("Email reachable profiles: " + email_push_no + "(" + email_push_perc + ")")
    datatable["Email Reachable Profiles"] = email_push_no

    wa_push_no = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[2]/div/div[5]/div[2]').text
    wa_push_perc = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[2]/div/div[5]/div[3]').text
    print("WhatsApp reachable profiles: " + wa_push_no + "(" + wa_push_perc + ")")
    datatable["WhatsApp Reachable Profiles"] = wa_push_no

    aud_push_no = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[2]/div/div[6]/div[2]').text
    aud_push_perc = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[2]/div/div[6]/div[3]').text
    print("Audiences reachable profiles: " + aud_push_no + "(" + aud_push_perc + ")")
    datatable["Audiences Push Reachable Profiles"] = aud_push_no

    did_event_xpath = "/html/body/div[6]/div[3]/div/div/div[5]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[4]/div[2]/div/button"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, did_event_xpath))).click()
    date_range_xpath = "/html/body/div[6]/div[3]/div/div/div[5]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[4]/ul/li/div[2]/div/div/div[1]/div[2]/span/div/div/span/div[1]"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,date_range_xpath))).click()
    time.sleep(3)
    last_x_days_path = "/html/body/div[6]/div[3]/div/div/div[5]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[4]/ul/li/div[2]/div/div/div[1]/div[2]/span/div/div/span/div[3]/div[3]/div[1]/div/div[3]/div/div/a/div"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,last_x_days_path))).click()
    time.sleep(3)
    last_7_days_path = "/html/body/div[6]/div[3]/div/div/div[5]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[4]/ul/li/div[2]/div/div/div[1]/div[2]/span/div/div/span/div[3]/div[3]/div[1]/div/div[3]/div/div/div/ul/li[7]"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,last_7_days_path))).click()
    apply_7_days_path = "/html/body/div[6]/div[3]/div/div/div[5]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[4]/ul/li/div[2]/div/div/div[1]/div[2]/span/div/div/span/div[3]/div[4]/button[2]"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,apply_7_days_path))).click()
    

    event_select_xpath = "/html/body/div[6]/div[3]/div/div/div[5]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[4]/ul/li/div[2]/div/div/div[1]/div[1]/div/div/a/div"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, event_select_xpath))).click()
    time.sleep(3)
    id_error_event_xpath = "/html/body/div[6]/div[3]/div/div/div[5]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[4]/ul/li/div[2]/div/div/div[1]/div[1]/div/div/div/ul/li[13]"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, id_error_event_xpath))).click()

    view_details_xpath = "/html/body/div[6]/div[3]/div/div/div[5]/div[1]/div[2]/input"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, view_details_xpath))).click()

    time.sleep(10)
    id_err_profiles = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[1]/div[2]').text
    print("Size of Identity Error profiles: " + id_err_profiles)
    datatable["Identity Error Profiles"] = id_err_profiles

    event_select_xpath = "/html/body/div[6]/div[3]/div/div/div[5]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[4]/ul/li/div[2]/div/div/div[1]/div[1]/div/div/a/div"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, event_select_xpath))).click()
    time.sleep(3)
    id_set_event_xpath = "/html/body/div[6]/div[3]/div/div/div[5]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[4]/ul/li/div[2]/div/div/div[1]/div[1]/div/div/div/ul/li[15]"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, id_set_event_xpath))).click()

    filter_by_elem_xpath = "/html/body/div[6]/div[3]/div/div/div[5]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[4]/ul/li/div[2]/div/div/div[2]/a"
    driver.find_element_by_xpath(filter_by_elem_xpath).click()

    prop_val_input_xpath = "/html/body/div[6]/div[3]/div/div/div[5]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[4]/ul/li/div[2]/div/div/div[3]/div[1]/div/span[2]/div[3]/div/input"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, prop_val_input_xpath))).send_keys('true,')

    view_details_xpath = "/html/body/div[6]/div[3]/div/div/div[5]/div[1]/div[2]/input"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, view_details_xpath))).click()

    time.sleep(10)
    id_set_profiles = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[1]/div[2]').text
    print("Size of Blacklisted profiles: " + id_set_profiles)
    datatable["Blacklisted Profiles"] = id_set_profiles

    fe_url = driver.current_url.replace("people","event")
    driver.get(fe_url)

    ev_last_30_days_xpath = "/html/body/div[6]/div[3]/div/div/div[6]/div[2]/div[1]"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, ev_last_30_days_xpath))).click()
    time.sleep(2)
    ev_last_7_days_xpath = "/html/body/div[6]/div[3]/div/div/div[6]/div[2]/div[2]/div[1]/ul/li[2]"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, ev_last_7_days_xpath))).click()
    
    event_area_xpath = "/html/body/div[6]/div[3]/div/div/div[9]/div[1]/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/div/div"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, event_area_xpath))).click()
    time.sleep(2)
    for element in driver.find_elements_by_tag_name("li"):
        if element.text == "App Launched" and element.is_displayed():
            element.click()
            break
    time.sleep(5)
    evt_number_xpath = "/html/body/div[6]/div[3]/div/div/div[9]/div[2]/div[1]/div[3]/div/div[1]"
    app_launched_count = driver.find_element_by_xpath(evt_number_xpath).text

    print("App Launched Count: " + app_launched_count)
    datatable["App Launched"] = app_launched_count

    event_area_xpath = "/html/body/div[6]/div[3]/div/div/div[9]/div[1]/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/div/div"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, event_area_xpath))).click()
    time.sleep(2)
    for element in driver.find_elements_by_tag_name("li"):
        if element.text == "App Uninstalled" and element.is_displayed():
            element.click()
            break

    time.sleep(5)
    evt_number_xpath = "/html/body/div[6]/div[3]/div/div/div[9]/div[2]/div[1]/div[3]/div/div[1]"
    app_uninstalled_count = driver.find_element_by_xpath(evt_number_xpath).text

    print("App Uninstalled Count: " + app_uninstalled_count)
    datatable["App Uninstalled"] = app_uninstalled_count

    event_area_xpath = "/html/body/div[6]/div[3]/div/div/div[9]/div[1]/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/div/div"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, event_area_xpath))).click()
    time.sleep(2)
    for element in driver.find_elements_by_tag_name("li"):
        if element.text == "Notification Sent" and element.is_displayed():
            element.click()
            break

    time.sleep(5)
    evt_number_xpath = "/html/body/div[6]/div[3]/div/div/div[9]/div[2]/div[1]/div[3]/div/div[1]"
    notif_sent_count = driver.find_element_by_xpath(evt_number_xpath).text

    print("Notification Sent Count: " + notif_sent_count)
    datatable["Notification Sent"] = notif_sent_count
    
    event_area_xpath = "/html/body/div[6]/div[3]/div/div/div[9]/div[1]/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/div/div"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, event_area_xpath))).click()
    time.sleep(2)
    for element in driver.find_elements_by_tag_name("li"):
        if element.text == "Notification Clicked" and element.is_displayed():
            element.click()
            break

    time.sleep(5)
    evt_number_xpath = "/html/body/div[6]/div[3]/div/div/div[9]/div[2]/div[1]/div[3]/div/div[1]"
    notif_clicked_count = driver.find_element_by_xpath(evt_number_xpath).text

    print("Notification Clicked Count: " + notif_clicked_count)
    datatable["Notification Clicked"] = notif_clicked_count

    event_area_xpath = "/html/body/div[6]/div[3]/div/div/div[9]/div[1]/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/div/div"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, event_area_xpath))).click()
    time.sleep(2)
    for element in driver.find_elements_by_tag_name("li"):
        if element.text == "Push Impressions" and element.is_displayed():
            element.click()
            break

    time.sleep(5)
    evt_number_xpath = "/html/body/div[6]/div[3]/div/div/div[9]/div[2]/div[1]/div[3]/div/div[1]"
    push_impression_count = driver.find_element_by_xpath(evt_number_xpath).text

    print("Push Impressions Count: " + push_impression_count)
    datatable["Push Impressions"] = push_impression_count

    charged_event_name = input("Enter conversion event: ")

    event_area_xpath = "/html/body/div[6]/div[3]/div/div/div[9]/div[1]/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/div/div"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, event_area_xpath))).click()
    time.sleep(2)
    event_found = False
    for element in driver.find_elements_by_tag_name("li"):
        if element.text == charged_event_name:
            element.click()
            event_found = True
            break
    
    if event_found == False:
        charged_event_name = "Charged"
        print("Conversion event entered not found, using Charged")

    time.sleep(5)
    evt_number_xpath = "/html/body/div[6]/div[3]/div/div/div[9]/div[2]/div[1]/div[3]/div/div[1]"
    charged_event_count = driver.find_element_by_xpath(evt_number_xpath).text

    print(charged_event_name + " Count: " + charged_event_count)
    datatable[charged_event_name] = charged_event_count
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