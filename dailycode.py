from urllib.request import urlretrieve 
import os
import re
import collections 

URL_PATH = 'https://s3.amazonaws.com/tcmg476/http_access_log'
LOCAL_FILE = 'local_copy.log'

#Use urlretrieve() to gech a remote copu and save into the local file path
local_file, headers = urlretrieve(URL_PATH, LOCAL_FILE)

i=0

redirectCounter = 0
errorCounter = 0

def file_len(LOCAL_FILE):
    with open (LOCAL_FILE) as f:
        for i, l in enumerate (f):
            pass
    return i + 1

print(file_len(LOCAL_FILE))
totalResponses = file_len(LOCAL_FILE)
print("Average requests per day: ", round(totalResponses/365,2))
print("Average requests per week: ",round(totalResponses/52,2))
print("Average requests per month:", round(totalResponses/12,2))