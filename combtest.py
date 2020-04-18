import requests
import json
from pyquery import PyQuery as pq
#from url_pag_add import url_addpag
import url_pag_add


def get_list_page_url(city, searchv):
    # start_url = "https://{}.lianjia.com/ershoufang/rs新凯%20长宁".format(city)
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
        print('URL:'+start_url)
        page_url_list = url_pag_add.url_addpag(start_url, total_page)
        return page_url_list

    except Exception as err:
        print("获取总套数出错,请确认起始URL是否正确")
        print("error message:" + err)
        return None
    finally:
        pass


def main():
    # cq,cs,nj,dl,wh,cc,sh
    city_list = ['sh']
    for city in city_list:
        page_url_list = get_list_page_url(city, '世纪公园')
        save_data(page_url_list, city)


def save_data(data, filename):
    with open(filename+".json", 'w', encoding="utf-8") as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    # old = time.time()
    main()
    # new  = time.time()
    # delta_time = new - old
    # print("程序共运行{}s".format(delta_time))
    print("finish.")
