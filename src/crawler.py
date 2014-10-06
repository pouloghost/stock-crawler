class DataLoader:
    def __init__(self, url):
        import http.client as httplib
        self.__connection = httplib.HTTPConnection(url)

    def fetch_data(self, code):
        self.__connection.request('GET', '/q=' + code)
        response = self.__connection.getresponse()
        return response.read().decode('gbk')
    def __del__(self):
        self.__connection.close()

class Stock:
    title = ['名字','代码','价格','昨收',\
             '今开','成交量','外盘','内盘',\
             '买一','买一量','买二','买二量',\
             '买三','买三量','买四','买四量',\
             '买五','买五量','卖一','卖一量',\
             '卖二','卖二量','卖三','卖三量',\
             '卖四','卖四量','卖五','卖五量',\
             '卖三','卖三量','卖四','卖四量',\
             '涨跌','涨跌幅','最高','最低',\
             '成交量','成交额','换手率','市盈率',\
             '最高','最低','振幅','流通值',\
             '市值','市净率']
    
    def __init__(self, string, code, now):
        self.__data = string.split('~')
        #is today's data
        if(-1 == self.__data[30].find(now)):
            self.__data = None
            return
        # remove some records
        del self.__data[47:50]
        del self.__data[40]
        del self.__data[35]
        del self.__data[29:31]
        del self.__data[0]
        self.__data[1] = code

    def get_data(self):
        return self.__data
    
def load_all(dicts, now):
    results = []
    loader = DataLoader('qt.gtimg.cn')
    i = 0
    for dict in dicts:
        print('market {0}'.format(i))
        i += 1
        j = 0
        total = len(dict)
        for key in dict:
            j += 1
            if(0 == j % 10):
                print('{0} in {1}'.format(j, total))
            data = Stock(loader.fetch_data(key), key, now).get_data()
            if(None == data):
                continue
            results.append(data)
                
    return results

def write_to_file(results, now):
    import csv
    out = open('../data/' + now + '.csv', 'w', newline='')
    writer = csv.writer(out)
    writer.writerow(Stock.title)
    writer.writerows(results)
    
if __name__ == '__main__':
    print(type(Stock.title))
    import sh, sz
    dicts = [sh.sh, sz.sz]
    import datetime
    now = datetime.datetime.now().strftime('%Y%m%d')
    results = load_all(dicts, now)
    if(not 0 == len(results)):
        write_to_file(results, now)
