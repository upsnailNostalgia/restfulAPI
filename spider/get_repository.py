import pymysql
import requests
from xml.dom.minidom import parse
import xml.dom.minidom
import re

def translate(data, input, output):
    for index in range(len(input)):
        data = data.replace(input[index], output[index])
    return data

def filter_tag(data, tag):
    data = data.split(tag)
    string = ''
    for item in data:
        if item in ('&quot;', '&amp;', '&lt;', '&gt;', '&nbsp;'):
            continue
        string += item
    return string

def filter_html(data):
    data = data.replace('\n', ' ')
    tag_pattern = '<(.*?)>'
    tag_list = re.findall(tag_pattern, data)
    for tag in tag_list:
        data = filter_tag(data, '<' + tag + '>')
    ret = ' '.join(data.split())
    input_table = ('&quot;', '&amp;', '&lt;', '&gt;', '&nbsp;')
    output_table = ('"', '&', '<', '>', ' ')
    ret = translate(ret, input_table, output_table)
    return ret

number = 3
index = 1
fields = ('title', 'description', 'summary', 'priority', 'assignee', 'reporter', 'label', 'status',
          'resolution', 'created', 'updated', 'component', 'votes', 'watches', 'type', 'version', 'fixVersion')
### 还有个type
conn = pymysql.connect(
     host = '10.131.252.160',
     db = 'github',
     user = 'root',
     passwd = 'root',
     charset = 'utf8mb4')

cur = conn.cursor()
sql = 'insert into issue (title, description, summary, priority, assignee, reporter, labels, ' \
      'created, updated, component, votes, watches, type, version, fixVersion, project, status, resolution)' \
      'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

project = 'LUCENE'

while True:
    if index > 8654:
        break

    path = 'd:/valysin/%s-%s.xml' % (number, index)
    try:
        DOMTree = xml.dom.minidom.parse(path)
    except:
        index += 1
        continue

    collection = DOMTree.documentElement
    items = collection.getElementsByTagName('item')

    for item in items:

        dic = {}

        for field in fields:
            if field == 'version' or field == 'fixVersion' or field == 'label':
                temp = []
                for element in item.getElementsByTagName(field):
                    temp.append(element.childNodes[0].data)

                value = ' '.join(temp)
                temp.clear()

            else:
                if len(item.getElementsByTagName(field)) == 0:
                    value = None
                else:
                    element = item.getElementsByTagName(field)[0]
                    if len(element.childNodes) == 0:
                        value = None
                    else:
                        if field == 'description':
                            value = filter_html(element.childNodes[0].data)
                        else:
                            value = element.childNodes[0].data


            dic[field] = value

        cur.execute(sql,
                    (dic['title'], dic['description'], dic['summary'], dic['priority'],
                     dic['assignee'], dic['reporter'], dic['label'], dic['created'],
                     dic['updated'], dic['component'], dic['votes'], dic['watches'],
                     dic['type'], dic['version'], dic['fixVersion'], project, dic['status'],
                     dic['resolution']))
        conn.commit()
        dic.clear()

    index += 1
