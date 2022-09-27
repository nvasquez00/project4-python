from urllib.request import urlretrieve
import os
import re
import collections

months_count = {"Jan": 0, "Feb": 0, "Mar": 0, "Apr": 0, "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 0, "Oct": 0,
                "Nov": 0, "Dec": 0}

janlogs = open("january.txt", "a+")
feblogs = open("february.txt", "a+")
marlogs = open("march.txt", "a+")
aprlogs = open("april.txt", "a+")
maylogs = open("may.txt", "a+")
junlogs = open("june.txt", "a+")
jullogs = open("july.txt", "a+")
auglogs = open("august.txt", "a+")
seplogs = open("september.txt", "a+")
octlogs = open("octlogs.txt", "a+")
novlogs = open("november.txt", "a+")
declogs = open("december.txt", "a+")

i = 0

redirectCounter = 0
errorCounter = 0
URL = 'https://s3.amazonaws.com/tcmg476/http_access_log'
LOCAL_FILE = 'http_access_log'


def file_len(LOCAL_FILE):
    with open(LOCAL_FILE) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def fileCount():
    filelog = []
    leastcommon = []
    with open(LOCAL_FILE) as logs:
        for line in logs:
            try:
                filelog.append(line[line.index("GET") + 4:line.index("HTTP")])
            except:
                pass
    counter = collections.Counter(filelog)
    for count in counter.most_common(1):
        print('\033[1m' +"Most commonly requested file: {} with {} requests.".format(str(count[0]), str(count[1])) + '\033[0m')
    for count in counter.most_common():
        if str(count[1]) == '1':
            leastcommon.append(count[0])
    if leastcommon:
        response = input(
            '\033[1m' + "Looks like there were {} file(s) that were requested only once, show all? (y/n)".format(len(leastcommon)) + '\033[0m')
        if response == 'y' or response == 'Y':
            for file in leastcommon:
                print(file)


if not os.path.isfile(LOCAL_FILE):
    urlretrieve(URL, LOCAL_FILE)

pattern = r'(.*?) - (.*) \[(.*?)\] \"(.*?) (.*?)\"? (.+?) (.+) (.+)'

lines = open(LOCAL_FILE, 'r').readlines()

# outside loop
days_result = []
date_counter = 0
current_date = "24/Oct/1994"

for line in lines:
    match = re.match(pattern, line)
    if not match:
        continue

    match.group(0)  # The original line
    match.group(3)  # The timestamp
    timestamp = match.group(3)
    month = timestamp[3:6]
    months_count[month] += 1
    match.group(7)  # The status codes

    # inside loop
    date = timestamp[0:11]
    if date == current_date:
        date_counter += 1
    else:
        days_result.append((current_date, date_counter))
        current_date = date
        date_counter = 1

    if match.group(7)[0] == "3":
        redirectCounter += 1
    elif match.group(7)[0] == "4":
        errorCounter += 1
    if month == "Jan":
        janlogs.write(line)
    elif month == "Feb":
        feblogs.write(line)
    elif month == "Mar":
        marlogs.write(line)
    elif month == "Apr":
        aprlogs.write(line)
    elif month == "May":
        maylogs.write(line)
    elif month == "Jun":
        junlogs.write(line)
    elif month == "Jul":
        jullogs.write(line)
    elif month == "Aug":
        auglogs.write(line)
    elif month == "Sep":
        seplogs.write(line)
    elif month == "Oct":
        octlogs.write(line)
    elif month == "Nov":
        novlogs.write(line)
    elif month == "Dec":
        declogs.write(line)

    else:
        continue
print('\033[1m' +"Total requests made:" + '\033[0m')
print(file_len(LOCAL_FILE))
totalResponses = file_len(LOCAL_FILE)
print('\033[1m' +"Average requests per day:" + '\033[0m', round(totalResponses / 365, 2))
for day in days_result:
    print(f"On {day[0]} there were {day[1]} requests")
print('\033[1m' + "Average requests per week:" + '\033[0m', round(totalResponses / 52, 2))
print('\033[1m' + "Average requests per month:" + '\033[0m', round(totalResponses / 12, 2))
print('\033[1m' + "Month Count:" + '\033[0m', months_count)
print('\033[1m' + "Total number of Errors:" + '\033[0m', errorCounter)
print('\033[1m' + "Percentage of client error (4xx) requests: " + '\033[0m' + "{0:.2%}".format(errorCounter / totalResponses))
print('\033[1m' + "Total number of redirects:" + '\033[0m', redirectCounter)
print('\033[1m' + "Percentage of all requests that were redirects (3xx): " + '\033[0m' + "{0:.2%}".format(redirectCounter / totalResponses))
fileCount()
