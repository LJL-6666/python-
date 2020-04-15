import requests
def getHTMLText():
    try:
        r = requests.get(url,timeout = 30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except;
        return''
url = 'http://www.baidu.com'
print(getHTMLText(url))
