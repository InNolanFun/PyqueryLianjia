import requests
import json
from pyquery import PyQuery as pq
import threading
from concurrent.futures import ThreadPoolExecutor
import time
# import local modue
import localdb
from url_pag_add import url_addpag
# 获取搜索结果


def get_list_page_url(city, searchv):
    start_url = "https://sh.lianjia.com/ershoufang/rs{}/".format(searchv)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }
    try:
        response = requests.get(start_url, headers=headers)
        textmsg = response.text
        doc = pq(textmsg)
        total_num = int(doc(".resultDes .total span").text())
        total_page = total_num // 30 + 1
        # 只能访问到前一百页
        if total_page > 100:
            total_page = 100
        print('Start URL:'+start_url)
        page_url_list = url_addpag(start_url, total_page)
        return page_url_list
    except Exception as err:
        print("获取总套数出错,请确认起始URL是否正确")
        print("error message:{}".format(err))
        return None
    finally:
        pass


def get_detail_page_url(page_url):
    global detail_list
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Referer': 'https://bj.lianjia.com/ershoufang'
    }

    try:
        response = requests.get(page_url, headers=headers, timeout=3)
        doc = pq(response.text)
        i = 0
        detail_urls = list()
        for item in doc(".sellListContent li").items():
            i += 1
            if i == 31:
                break
            child_item = item(".noresultRecommend")
            if child_item == None:
                i -= 1
            detail_url = child_item.attr("href")
            detail_urls.append(detail_url)
        return detail_urls
    except Exception as ex:
        print("获取列表页'{}'报错".format(page_url))
        print('ErrorMessage:{}'.format(ex))


lock = threading.Lock()

# 获取详细信息


def detail_page_parser(res):
    global detail_list
    global runcount
    global allpage
    detail_urls = res.result()
    if not detail_urls:
        print("detail url 为空")
        return None
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Referer': 'https://sh.lianjia.com/ershoufang'
    }
    for detail_url in detail_urls:
        try:
            response = requests.get(url=detail_url, headers=headers, timeout=3)
            detail_dict = dict()
            doc = pq(response.text)
            # 单价
            unit_price = doc(".unitPriceValue").text()
            unit_price = unit_price[0:unit_price.index("元")]
            if len(unit_price) > 0:
                detail_dict['unit_price'] = unit_price
                # 总价
                detail_dict['all_price'] = doc('.price .total').text().strip()
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
                # 小区
                detail_dict['community'] = doc(
                    ".communityName .info").text().strip()
                # 区域
                va = doc(".areaName .info a")
                detail_dict['location'] = '\t'.join(
                    [va.eq(x).text().strip() for x in range(len(va))])
                # URL
                detail_dict["url"] = detail_url
                detail_list.append(detail_dict)
        except Exception as ex:
            print("获取详情页出错,URL:{}".format(detail_url))
            print('error message:{}'.format(ex))
            return None


def main():
    # cq,cs,nj,dl,wh,cc,sh
    city_list = ['sh']
    searchvalue_list = ['世纪公园', '花木苑']
    for city in city_list:
        for sev in searchvalue_list:
            page_url_list = get_list_page_url(city, sev)
            # 启动线程
            with ThreadPoolExecutor(30) as p:
                for page_url in page_url_list:
                    p.submit(get_detail_page_url, page_url).add_done_callback(
                        detail_page_parser)
            # 保存数据
            # save_data(detail_list, 'city_{}_search_{}'.format(city, sev))
            tablename = 'shanghai'
            localdb.createdb(tablename)
            localdb.insertdatatodb(detail_list, tablename)
        detail_list.clear()
    
    count = 0
    for i in localdb.searchdata('shanghai'):
        print(i)
        count +=1
        if count == 100:
            break

def save_data(data, filename):
    with open(filename+".json", 'w', encoding="utf-8") as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False))


#global p
detail_list = list()
if __name__ == '__main__':
    old = time.time()
    main()
    new = time.time()
    delta_time = new - old
    print("程序共运行{}s".format(delta_time))
