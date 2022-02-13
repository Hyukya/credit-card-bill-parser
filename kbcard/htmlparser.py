from html.parser import HTMLParser
import copy
import sys
import json

class KBCardHTMLParser(HTMLParser):
    data_list = []
    full_tag = []

    def handle_starttag(self, tag, attrs):
        if tag in ['meta', 'br']:
            return
        self.full_tag.append(tag)

    def handle_endtag(self, tag):
        if tag in ['meta', 'br']:
            return
        self.full_tag.pop()

    def handle_data(self, data):
        data = data.strip()
        self.data_list.append({'tag':copy.deepcopy(self.full_tag), 'data':data})
    
    def parse(self, filepath):
        f = open(filepath, 'r', encoding='EUC-KR')
        html_data = f.read()
        f.close()

        이용내역_rawdata = html_data[html_data.index('<!--<ON-NULL-DEL-이용내역>-->')+len('<!--<ON-NULL-DEL-이용내역>-->'):html_data.rindex('<!--<ON-NULL-DEL-이용내역>-->')]
        이용내역_jsonstring = 이용내역_rawdata[이용내역_rawdata.index('['):이용내역_rawdata.rindex(';')]
        이용내역_jsonstring = 이용내역_jsonstring.replace('\n', '')
        if ',' == 이용내역_jsonstring[len(이용내역_jsonstring)-2]:
            tmp = list(이용내역_jsonstring)
            tmp[len(tmp)-2] = ''
            이용내역_jsonstring = ''.join(tmp)
        이용내역_jsonstring = 이용내역_jsonstring.replace('"', '\'')
        이용내역_jsonstring = 이용내역_jsonstring.replace('\'<', '"<')
        이용내역_jsonstring = 이용내역_jsonstring.replace('>\'', '>"')
        이용내역_jsonstring = 이용내역_jsonstring.replace('\'data\'', '"data"')
        이용내역_jsonstring = 이용내역_jsonstring.replace('\'청구일련번호\'', '"청구일련번호"')

        이용내역_json = json.loads(이용내역_jsonstring.encode('utf8'))
        이용내역_json = filter(lambda i : 0 == i['data'].count('colspan='), 이용내역_json)
        
        self.feed(''.join(map(lambda i: i['data'], 이용내역_json)))
        
        only_details = map(lambda i: i['data'], self.data_list)
        index_order = ['이용일자','이용카드','구분','이용하신_가맹점','포인트리_스타샵(적립)_가맹점','이용금액','할부개월','이번달결제금액_회차','이번달결제금액_원금','이번달결제금액_수수료','결제후잔액_회차','결제후잔액_원금','적립예정포인트리']
        
        result = dict(unknown=[], 내역=[])

        temp_dict = dict()
        idx = 0
        for data in only_details:
            if idx == len(index_order):
                result['내역'].append(temp_dict)
                temp_dict = dict()
                idx = 0
            temp_dict[index_order[idx]] = data
            idx = idx + 1
        if idx == len(index_order):
            result['내역'].append(temp_dict)
            temp_dict = dict()
            idx = 0

        return result

if __name__ == "__main__":
    if len(sys.argv) < 1:
        exit(1)

    parser = KBCardHTMLParser()
    result = parser.parse(sys.argv[1])
    
    print(result)
    print('내역')
    for i in result['내역']:
        print(i['이용일자'], i['이용하신_가맹점'], i['이용금액'])
        pass

    exit(0)