## 获得列表
def get_list(i,j):
    attempts = 0
success = False
while attempts < 5 and not success:
    try:
        url = 'https://search.bilibili.com/all?keyword=%E7%BC%96%E7%A8%8B&from_source=banner_search&order={}&duration=4&tids_1=36&page={}'.format(i,j+1) 
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win32; x32; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Connection': 'keep-alive'}
        cookies ='v=3; iuuid=1A6E888B4A4B29B16FBA1299108DBE9CDCB327A9713C232B36E4DB4FF222CF03; webp=true; ci=1%2C%E5%8C%97%E4%BA%AC; __guid=26581345.3954606544145667000.1530879049181.8303; _lxsdk_cuid=1646f808301c8-0a4e19f5421593-5d4e211f-100200-1646f808302c8; _lxsdk=1A6E888B4A4B29B16FBA1299108DBE9CDCB327A9713C232B36E4DB4FF222CF03; monitor_count=1; _lxsdk_s=16472ee89ec-de2-f91-ed0%7C%7C5; __mta=189118996.1530879050545.1530936763555.1530937843742.18'
        cookie = {}
        for line in cookies.split(';'):
            name, value = cookies.strip().split('=', 1)
            cookie[name] = value 
            html = requests.get(url,cookies=cookie, headers=header).content
            bsObj = BeautifulSoup(html.decode('utf-8'),"html.parser")
            script = bsObj.find_all('script')[3].text
            info = json.loads(script.replace('window.__INITIAL_STATE__=','').split(';(function()')[0])['allData']['video']
        return info
        except:
            attempts = attempts+1
        return []

coding_all = []
type = ['click','stow','dm']
for i in type:
    for j in range(50):
        this_coding = get_list(i,j)
        coding_all = coding_all+this_coding
