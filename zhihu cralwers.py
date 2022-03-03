import re
import urllib.request, urllib.error
from bs4 import BeautifulSoup
import xlwt

findtitle = re.compile(r'<h2 class="HotItem-title">(.*?)</h2>')
findexcerpt = re.compile(r'</h2>(.*?)</a>', re.S)
#findimg = re.compile(r'src="(.*?)"/>')
findimg = re.compile(r'</span></div></div>(.*?)</section>', re.S)
def main():
    url ='https://www.zhihu.com/hot'
    url = askurl(url)
    data = getData(url)
    file = "知乎热榜.xls"
    saveData(data, file)


def askurl(url):
    data = {

    }
    head = {
        # ':authority': 'www.zhihu.com',
        # ':method': 'GET',
        # ':path': '/hot',
        # ':scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        # 'accept-encoding': 'gzip, deflate, br',
        # 'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': '_zap=83938e53-3729-4c08-801b-33b4c637aebf; _xsrf=2b790c0e-e34c-41f2-8ae6-7845c2c10d7e; d_c0="AGBf_q6goxGPTp9j8ViM3BOBux8pb4NRIoo=|1595818643"; _ga=GA1.2.522696158.1595818644; _gid=GA1.2.243299162.1595818644; l_n_c=1; n_c=1; tshl=; tst=h; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1595818643,1595818926; SESSIONID=qThpmePce5dzddkpvjL5GGWaM0ej6UA5t3ySjZRztDv; JOID=UFwQBU_KU0HvScKIPs5jnbf4ZisovQYqnSKh2V6pYCSWL6DlT2ISXrRJxYo_rgM2Ea_F4Eq0p8xugVE9GIYPyhw=; osd=VFAWAEnOX0fqT8aEOMtlmbv-Yy0ssQAvmyat31uvZCiQKqbhQ2QXWLBFw485qg8wFKnB7Eyxochih1Q7HIoJzxo=; capsion_ticket="2|1:0|10:1595828280|14:capsion_ticket|44:N2IyNjMyYTkzNDZkNGNiM2FhMjVlYWNjNjc0MmNhNmU=|ec5bf5165cfd8fdb9afc6902c5ab132c7df571da8e576e5859fc995f240a96cf"; _gat_gtag_UA_149949619_1=1; r_cap_id="MDZmMjA5NWQ0YzQwNGYzMmI3ODRjNzQwYmMxYTg5NzU=|1595828293|2a9c56f0fd4a24e1ad53b93e32601ff70fc7979a"; cap_id="ODgzM2YzNWQ0NDUwNGYzYzg0MjVhNTAwNGVlODZmMDE=|1595828293|7d1776ca8681e986347b1e77ac6cdc414a88675f"; l_cap_id="YjZiNmVmZGU3MmFhNDliYzk1NjUzOTZkYTM0YjZhMjQ=|1595828293|b2d142a4336b570596e14e312ea578b8166e8d62"; z_c0=Mi4xcjBhV0V3QUFBQUFBWUZfLXJxQ2pFUmNBQUFCaEFsVk5UN1lMWUFCemF4Z1JMWEtvdllFQWVGdDE1dmZKZWZhd0hR|1595828303|52a28c8e1d7a7186c625b807cb422c2464bd47de; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1595828306; KLBRSID=b33d76655747159914ef8c32323d16fd|1595828307|1595828279',
        'referer': 'https://www.zhihu.com/signin?next=%2Fhot',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
    }
    request = urllib.request.Request(url, headers=head)
    print(request)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def getData(url):
    datalist = []
    for i in range(0, 50):
        soup = BeautifulSoup(url, "html.parser")
        for item in soup.find_all('div', class_="HotList-list"):
            data = []
            item = str(item)
            # print(item)
            id = str(i+1)
            data.append(id)
            # print(id)
            title = re.findall(findtitle, item)[i]
            data.append(title)
            # print(title)
            excerpt = re.findall(findexcerpt, item)[i]
            excerpt = re.sub('<p class="HotItem-excerpt">|</p>', '', excerpt)
            data.append(excerpt)
            # print(excerpt)
            img = re.findall(findimg, item)[i]
            img = re.sub('<a class="HotItem-img"|data-za-not-track-link="true"|href=".*?"|rel="noopener noreferrer"|target="_blank"|title=".*?">|<img alt=".*?"|src=|"|/>|</a>| ', '', img)
            data.append(img)
            # print(img)
            datalist.append(data)
            # print(datalist)
    return datalist

def saveData(data, file):
    # da = data[0]
    # print(da)
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet("知乎热榜", cell_overwrite_ok=True)
    col = ("名次", "标题", "详细片段" ,"图片链接")
    for i in range(0, 4):
        sheet.write(0, i, col[i])
    for i in range(0, 50):
        datalist = data[i]
        for j in range(0, 4):
            sheet.write(i+1, j, datalist[j])

    book.save(file)



if __name__ == '__main__':
    main()