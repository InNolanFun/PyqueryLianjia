import requests
from pyquery import PyQuery as pq


# URL: https://sh.lianjia.com/ershoufang/107102321501.html
def detail_page_parser(detail_url):
    detail_list = list()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Referer': 'https://sh.lianjia.com/ershoufang'
    }
    try:
        response = requests.get(url=detail_url, headers=headers, timeout=3)
        detail_dict = dict()
        doc = pq(response.text)
        # 标题
        detail_dict["title"] = doc("h1").text()
        # 室
        detail_dict['rome'] = doc('.room .mainInfo').text()
        # 面积
        area = doc('.area .mainInfo').text()
        detail_dict['area'] = area[0:area.index("平")]
        # 年份
        buildyear = doc('.area .subInfo').text()
        detail_dict['buildyear'] = buildyear[0:buildyear.index('年')]
        # 单价
        unit_price = doc(".unitPriceValue").text()
        detail_dict['unit_price'] = unit_price[0:unit_price.index("元")]
        # 总价
        detail_dict['all_price'] = doc('.price .total').text().strip()
        # 小区
        detail_dict['community'] = doc(".communityName .info").text().strip()
        # 区域
        va = doc(".areaName .info a")
        detail_dict['location'] = '\t'.join(
            [va.eq(x).text().strip() for x in range(len(va))])
        detail_list.append(detail_dict)
    except Exception as ex:
        print("获取详情页出错,URL:{}".format(detail_url))
        print('error message:{}'.format(ex))


def save_local(data, filename):
    with open('{}.html'.format(filename), 'w', encoding="utf-8") as f:
        f.write(str(data))


def main():
    url = 'https://sh.lianjia.com/ershoufang/107102321501.html'
    detail_page_parser(url)


if __name__ == "__main__":
    main()
    print('finish.')
