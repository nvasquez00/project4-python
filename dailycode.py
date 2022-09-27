from urllib.request import urlretrieve 
import os
import re
import collections 

URL_PATH = 'https://s3.amazonaws.com/tcmg476/http_access_log'
LOCAL_FILE = 'local_copy.log'

#Use urlretrieve() to gech a remote copu and save into the local file path
local_file, headers = urlretrieve(URL_PATH, LOCAL_FILE)

months_count ={"Jan": 0, "Feb": 0, "Mar": 0, "Apr": 0, "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 0, "Oct": 0, "Nov": 0, "Dec": 0}

janlogs=open("january.txt", "a+"); feblogs=open("february.txt", "a+"); marlogs=open("march.txt", "a+"); 
aprlogs=open("april.txt", "a+"); maylogs=open("may.txt", "a+"); junlogs=open("june.txt", "a+");
jullogs=open("july.txt", "a+"); auglogs=open("august.txt", "a+"); seplogs=open("september.txt", "a+")
octlogs=open("octlogs.txt", "a+"); novlogs=open("november.txt", "a+"); declogs=open("december.txt", "a+")   


i=0

redirectCounter = 0
errorCounter = 0

def file_len(LOCAL_FILE):
    with open (LOCAL_FILE) as f:
        for i, l in enumerate (f):
            pass
    return i + 1

pattern = r'(.*?) - (.*) \[(.*?)\] \"(.*?) (.*?)\"? (.+?) (.+) (.+)'

lines = open(LOCAL_FILE, 'r').readlines()

#outside loop
days_result = []
date_counter = 0
current_date = "24/Oct/1994"

for line in lines:
    match = re.match(pattern, line)
    if not match:
        continue

    match.group(0) # The original line
    match.group(3) # The timestamp
    timestamp = match.group(3)
    month = timestamp[3:6]
    months_count[month] += 1
    match.group(7) # The status codes
    
    #inside loop
    date = timestamp[0:11]
    if date == current_date:
        date_counter += 1
    else:
        days_result.append((current_date, date_counter))
        current_date = date
        date_counter = 1 

    if (match.group(7)[0] == "3"):
        redirectCounter += 1
    elif (match.group(7)[0] == "4"):
        errorCounter += 1
    if (month == "Jan"): 
        janlogs.write(line)
    elif (month == "Feb"): 
        feblogs.write(line)
    elif (month == "Mar"): 
        marlogs.write(line)
    elif (month == "Apr"): 
        aprlogs.write(line)
    elif (month == "May"): 
        maylogs.write(line)
    elif (month == "Jun"): 
        junlogs.write(line)
    elif (month == "Jul"): 
        jullogs.write(line)
    elif (month == "Aug"): 
        auglogs.write(line)
    elif (month == "Sep"): 
        seplogs.write(line)
    elif (month == "Oct"): 
        octlogs.write(line)
    elif (month == "Nov"): 
        novlogs.write(line)
    elif (month == "Dec"): 
        declogs.write(line)
    
    else:
        continue
print("Total requests made:")
print(file_len(LOCAL_FILE))
totalResponses = file_len(LOCAL_FILE)
print("Average requests per day: ", round(totalResponses/365,2))
for day in days_result:
    print(f"On {day[0]} there were {day[1]} requests")
print("Average requests per week:",round(totalResponses/52,2))
print("Average requests per month:", round(totalResponses/12,2))
print("Month Count:", months_count)
