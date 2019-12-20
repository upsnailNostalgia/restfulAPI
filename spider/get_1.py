import time

import requests

MAX = 1965

LOG_PATH = 'd:/valysin/log.txt'
PREFIX = 'd:/valysin/1-'
PROJECT = 'HTTPCLIENT'

index = 554
base = 'https://issues.apache.org/jira/si/jira.issueviews:issue-xml/%s-%s/%s-%s.xml'

flag = 1

while True:

    if index > MAX:
        break

    url = base % (PROJECT, index, PROJECT, index)
    print(index)

    try:
        response = requests.get(url, timeout=30)

    except Exception as e:

        with open(LOG_PATH, 'a') as f:

            if flag > 3:
                info = '[%s] %s : url\n' % (time.ctime(time.time()), e.__str__())
                f.write(info)
                continue

            else:
                info = '[%s] %s\n' % (time.ctime(time.time()), e.__str__())
                f.write(info)

        time.sleep(180 * flag * flag)

        flag += 1

    else:

        flag = 1
        if response.status_code != 200:
            time.sleep(60)
            continue

        xml_data = response.text
        with open(PREFIX + str(index) + '.xml', 'w') as f:
            f.write(xml_data)

        index += 1