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
import datetime
import gspread   
import json

regions = ["eu","in","sg","us","sk"]
account_id = ""
region = ""
charged_event_name = ""
sheet_id = ""

if len(sys.argv) != 9:
    sys.exit("Arguments Entry Invalid. Sample usage: python3 simple.py -a ZWW-WWW-WWWZ -r eu -e 'ABC CDF' -s <Google Spreadsheet ID>")

arg_index = 0
account_id_found = False
region_found = False
special_event_found = False
sheet_id_found = False
while arg_index < len(sys.argv):
    if sys.argv[arg_index] == "-a" and (arg_index+1) != len(sys.argv):
        account_id = sys.argv[arg_index+1]
        account_id_found = True
    if sys.argv[arg_index] == "-r" and (arg_index+1) != len(sys.argv):
        region = sys.argv[arg_index+1]
        region_found = True
    if sys.argv[arg_index] == "-e" and (arg_index+1) != len(sys.argv):
        charged_event_name = sys.argv[arg_index+1]
        special_event_found = True
    if sys.argv[arg_index] == "-s" and (arg_index+1) != len(sys.argv):
        sheet_id = sys.argv[arg_index+1]
        sheet_id_found = True
    arg_index += 1

if(account_id_found == False or region_found == False or special_event_found == False or sheet_id_found == False):
    sys.exit("Arguments Entry Invalid. Sample usage: python3 simple.py -a ZWW-WWW-WWWZ -r eu -e 'ABC CDF' -s <Google Spreadsheet ID>")

if len(account_id) != 12 or account_id[3] != '-' or account_id[7] != '-' :
    sys.exit("Invalid Account Id Entered")
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
chrome_options.add_argument("user-data-dir=" + os.getcwd()+"/googlefiles")
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
    timestamp = datetime.datetime.now()
    datatable["Time"] = timestamp.strftime("%x") + " " + timestamp.strftime("%X")

    WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[3]/div/div/div[5]/div[1]/div[2]/input'))).click()
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
    for element in driver.find_elements_by_tag_name("li"):
        if element.text == "Identity Error" and element.is_displayed():
            element.click()
            break

    view_details_xpath = "/html/body/div[6]/div[3]/div/div/div[5]/div[1]/div[2]/input"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, view_details_xpath))).click()

    time.sleep(10)
    id_err_profiles = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[8]/div[1]/div[3]/div[3]/div[1]/div[2]').text
    print("Size of Identity Error profiles: " + id_err_profiles)
    datatable["Identity Error Profiles"] = id_err_profiles

    event_select_xpath = "/html/body/div[6]/div[3]/div/div/div[5]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[4]/ul/li/div[2]/div/div/div[1]/div[1]/div/div/a/div"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, event_select_xpath))).click()
    time.sleep(3)
    for element in driver.find_elements_by_tag_name("li"):
        if element.text == "Identity Set" and element.is_displayed():
            element.click()
            break

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
    cal_text_xpath = "/html/body/div[6]/div[3]/div/div/div[6]/div[2]/div[1]/span"
    cal_text = driver.find_element_by_xpath(cal_text_xpath).text
    if "Between" in cal_text:
        back_icon_xpath = "/html/body/div[6]/div[3]/div/div/div[6]/div[2]/div[3]/div[1]/img"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, back_icon_xpath))).click()
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
        print("Conversion event entered '%s' not found, using Charged" % charged_event_name)
        charged_event_name = "Charged"
        

    for element in driver.find_elements_by_tag_name("li"):
        if element.text == charged_event_name:
            element.click()
            break

    time.sleep(5)
    evt_number_xpath = "/html/body/div[6]/div[3]/div/div/div[9]/div[2]/div[1]/div[3]/div/div[1]"
    charged_event_count = driver.find_element_by_xpath(evt_number_xpath).text

    print(charged_event_name + " Count: " + charged_event_count)
    datatable[charged_event_name] = charged_event_count
    
    gc = gspread.service_account(filename=os.getcwd() + "/automation-1608644218205-e292924471e1.json")
    sheet = gc.open_by_key(sheet_id)
    worksheet_found = False
    acc_worksheet = sheet.get_worksheet(0)
    print("Adding data into Google Sheet with id: " + sheet_id)

    for worksheet in sheet.worksheets():
        if worksheet.title == account_id:
            worksheet_found = True
            acc_worksheet = worksheet
            row = acc_worksheet.row_count + 1
            acc_worksheet.add_rows(1)
            index = 1
            for key in datatable.keys():
                acc_worksheet.update_cell(row, index, datatable[key])
                index += 1

    if worksheet_found == False:
        acc_worksheet = sheet.add_worksheet(title=account_id, rows="2", cols="100")
        index = 1
        for key in datatable.keys():
            acc_worksheet.update_cell(1, index, key)
            acc_worksheet.update_cell(2, index, datatable[key])
            index += 1
    print ("1 row successfully inserted")
except: 
    print("Something went wrong. Please log and contact the dev")
    input("Press enter to continue")
finally:
    driver.quit()