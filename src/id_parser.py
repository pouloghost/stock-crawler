import re
# data from http://bbs.10jqka.com.cn/codelist.html
# format is roughly Chinese_name space id space next one
def parse_stock_ids(string, prefix):
    result = {}
    parts = string.split()
    last = ''
    number = re.compile(r'^\d*$')
    for part in parts:
        if(number.match(part)):
            result[prefix + part] = last
            last = ''
        else:
            last += part
    return result

def read_file(prefix):
    file = open('../other/' + prefix + '_origin.txt', 'r', encoding = 'utf-8')
    string = None
    try:
        string = file.read()
    finally:
        file.close()
    return string

def parse_to_file(string, prefix):
    file = open(prefix + '.py', 'w', encoding = 'utf-8')
    file.write('{0}={1}'.format(prefix, parse_stock_ids(string, prefix)))
    file.close()

def load_all(prefixs):
    for prefix in prefixs:
        print(prefix + '\n')
        string = read_file(prefix)
        if(None == string):
            continue
        print('after read \n')
        parse_to_file(string, prefix)
        print('write done \n')

if __name__ == '__main__':
    PREFIXS = ['sh', 'sz']
    load_all(PREFIXS)
