import json
from apiclient import discovery
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from bs4 import BeautifulSoup
import re
import time
import dateutil.parser as parser
from datetime import datetime
import csv

# Creating a storage.JSON file with authentication details
SCOPES = 'https://www.googleapis.com/auth/gmail.modify' 
store = file.Storage('storage.json') 
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

user_id = 'me'
label_id_one = 'INBOX'
label_id_two = 'UNREAD'

unread_msgs = GMAIL.users().messages().list(userId='me', labelIds=[label_id_one, label_id_two]).execute()
mssg_list = unread_msgs['messages']

print("Total unread messages in inbox: ", str(len(mssg_list)))

final_list = []

for index, mssg in enumerate(mssg_list):
    if index >= 10:
        break  # Stop processing after the first 10 emails

    temp_dict = {}
    m_id = mssg['id']
    message = GMAIL.users().messages().get(userId=user_id, id=m_id).execute()
    payld = message['payload']
    headr = payld['headers']

    for one in headr:
        if one['name'] == 'Subject':
            msg_subject = one['value']
            temp_dict['Subject'] = msg_subject
        else:
            pass

    for two in headr:
        if two['name'] == 'Date':
            msg_date = two['value']
            date_parse = parser.parse(msg_date)
            m_date = date_parse.date()
            temp_dict['Date'] = str(m_date)
        else:
            pass

    for three in headr:
        if three['name'] == 'From':
            msg_from = three['value']
            temp_dict['Sender'] = msg_from
        else:
            pass

    temp_dict['Snippet'] = message['snippet']

    try:
        mssg_parts = payld['parts']
        part_one = mssg_parts[0]
        part_body = part_one['body']
        part_data = part_body['data']
        clean_one = part_data.replace("-", "+")
        clean_one = clean_one.replace("_", "/")
        clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))
        soup = BeautifulSoup(clean_two, "lxml")
        mssg_body = soup.body()
        temp_dict['Message_body'] = mssg_body

    except:
        pass

    print(temp_dict)
    final_list.append(temp_dict)
    GMAIL.users().messages().modify(userId=user_id, id=m_id, body={'removeLabelIds': ['UNREAD']}).execute()

print("Total messages retrieved: ", str(len(final_list)))

# Exporting the values as .csv
with open('CSV_NAME.csv', 'w', encoding='utf-8', newline='') as csvfile:
    fieldnames = ['Sender', 'Subject', 'Date', 'Snippet', 'Message_body']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
    writer.writeheader()
    for val in final_list:
        writer.writerow(val)
