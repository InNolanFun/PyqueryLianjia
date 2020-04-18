
def main():
    page_url_list = "test"
    city = "SH"
    save_data(page_url_list, city)

  #      detail_list.clear()
def save_data(data,filename):
    with open(filename+".json", 'w', encoding="utf-8") as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    # old = time.time()
    main()
    # new  = time.time()
    # delta_time = new - old
    # print("程序共运行{}s".format(delta_time))
    print("finish.")