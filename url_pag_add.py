from urllib.parse import urlsplit
from urllib.parse import urljoin
import os

def url_addpag(detailurl, cot):
    urlsp = urlsplit(detailurl)
    urlsppth = [i for i in urlsp.path.split('/') if i != '']
    i = 1
    resulturllst = []
    while(i <= cot):
        sp = ''
        for j in urlsppth:
            if j == urlsppth[len(urlsppth)-1] and i != 1:
                # 搜索的Path为最后一个值前面增加 pgi 页码
                sp = os.path.join(sp,'pg{}{}'.format(str(i), urlsppth[len(urlsppth)-1]))
            else:
                sp = os.path.join(sp,j)
        resulturl = urljoin('{0}://{1}'.format(urlsp.scheme, urlsp.netloc), sp)
        i = i+1
        resulturllst.append(resulturl)
    return resulturllst

def main():
    url = 'https://sh.lianjia.com/ershoufang/rs7/'
    url_addpag(url, 6)

if __name__ == "__main__":
    main()
