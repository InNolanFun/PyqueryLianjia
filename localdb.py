import sqlite3


def createdb(tablename):
    with sqlite3.connect('example.db') as conn:
        c = conn.cursor()
        sql = '''CREATE TABLE if not exists {}
            (
                url text PRIMARY KEY,
                unit_price text,
                all_price text,
                title text,
                rome text,
                area text,
                buildyear text,
                community text,
                location text
            )
            '''.format(tablename)
        c.execute(sql)
        conn.commit()


def insertdatatodb(data, tablename):
    sql = '''INSERT INTO
                {}(
                    url,
                    unit_price,
                    all_price,
                    title,
                    rome,
                    area,
                    buildyear,
                    community,
                    location
                )
                VALUES(
                    :url,
                    :unit_price,
                    :all_price,
                    :title,
                    :rome,
                    :area,
                    :buildyear,
                    :community,
                    :location
                )
                ON CONFLICT(url) 
                    DO UPDATE SET 
                        unit_price=:unit_price,
                        all_price=:all_price,
                        title=:title,
                        rome=:rome,
                        area=:area,
                        buildyear=:buildyear,
                        community=:community,
                        location=:location
            '''.format(tablename)
    with sqlite3.connect('example.db') as conn:
        c = conn.cursor()
        for i in data:
            c.execute(sql, i)
        conn.commit()


def searchdata(tablename):
    sql = '''select * from {}'''.format(tablename)
    with sqlite3.connect('example.db') as conn:
        c = conn.cursor()
        va = c.execute(sql)
        return va


def moduletest():
    tablename = 'testtable'
    createdb(tablename)

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
    insertdatatodb(ls, tablename)
    for i in localdb.searchdata(tablename):
        print(i)


if __name__ == "__main__":
    moduletest()
