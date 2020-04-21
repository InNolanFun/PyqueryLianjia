from concurrent.futures import ThreadPoolExecutor
import requests
from pyquery import PyQuery as pq


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }

def querymsg(url, quent1, quent2):
    respon = requests.get(url,headers=headers)
    print(url)
    print(quent1)
    print(quent2)
    doc = pq(respon.text)

    return doc

def main(url):
    with ThreadPoolExecutor(5) as p:
        print(p.submit(querymsg,url,'quent1'))

if __name__ == "__main__":
    main('http://www.baidu.com')
    print('直接调用')
    querymsg('http://www.baidu.com','test1','test2')