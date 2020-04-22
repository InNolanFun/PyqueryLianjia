import localdb


def main():
    tablename = 'testtable'
    localdb.createdb(tablename)

    ls = list()
    for i in range(10):
        detail_dict = dict()
        # 单价
        detail_dict['unit_price'] = 'unit_price{}'.format(i)
        # 总价
        detail_dict['all_price'] = 'all_price{}'.format(i)
        # 标题
        detail_dict["title"] = 'title{}'.format(i)
        # 室
        detail_dict['rome'] = 'rome{}'.format(i)
        # 面积
        detail_dict['area'] = 'area{}'.format(i)
        # 年份
        detail_dict['buildyear'] = 'buildyear{}'.format(i)
        # 小区
        detail_dict['community'] = 'community{}'.format(i)
        # 区域
        detail_dict['location'] = 'location{}'.format(i)
        # URL
        detail_dict["url"] = 'url{}'.format(i)
        ls.append(detail_dict)
    localdb.insertdatatodb(ls, tablename)
    for i in localdb.searchdata(tablename):
        print(i)

if __name__ == "__main__":
    main()
