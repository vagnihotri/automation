# Script to fetch Key Account Metrics

This Python script uses Selenium to automate querying Account Metrics from the CleverTap dashboard **for the past 7 days**.
It queries the following account metrics from the past 7 days sequentially and then sends it to a Google Sheet -
1. Size of All Users Segment
2. Reachability of All Users Segment on Web Push, Email, Push, SMS, Whatsapp, and Audiences channels
3. Blacklisting Profile count (Identity Set -> Dropped History -> true)
4. Identity Error Profile count
5. App Launched Event Count
6. App Uninstalled Event Count
7. Notification Sent Event Count
8. Notification Clicked Event Count
9. Push Impression Event Count
10. Key Account Event Count (Typically the conversion event for the account for example, Charged.)

# Usage 
Please exit Google Chrome Browser<br><br>

**Using source code** <br>
(After installing pip3, selenium and gspread) - <br>
`python3 script.py -a 989-WZK-K45Z -r eu -e 'Subscribed' -s <Google Spreadsheet ID>`<br>
**Using the bundled executable (Mac OS only)** <br>
(Make sure the kam_script and chromedriver executables are in the same directory) <br>
`./kam_script -a 989-WZK-K45Z -r eu -e 'Subscribed' -s <Google Spreadsheet ID>` <br>
If Mac OS blocks it, please follow the steps mentioned [here](https://support.apple.com/en-in/HT202491) <br><br>
Where a 12 character Account Id, Account Region, Key Event and Google Spreadsheet ID are passed as arguments (-a, -r, -e, -s respectively). 
If the Key Event entered isn't found, Charged is used by default

# Requirements:
1. Access to accounts
2. Have to log in using MFA the first time the script is used in a session
3. Google Sheet access - open your Google Sheet and give Editor access to automation@automation-1608644218205.iam.gserviceaccount.com (If building from source, please edit line #280 with your id)
