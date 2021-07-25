from html.parser import HTMLParser
import copy
import sys

class LotteCardHTMLParser(HTMLParser):
    data_list = []
    full_tag = []

    def handle_starttag(self, tag, attrs):
        if tag == 'meta':
            return
        self.full_tag.append(tag)

    def handle_endtag(self, tag):
        if tag == 'meta':
            return
        self.full_tag.pop()

    def handle_data(self, data):
        data = data.strip()
        self.data_list.append({'tag':copy.deepcopy(self.full_tag), 'data':data})
    
    def parse(self, filepath):
        f = open(filepath, 'r', encoding='UTF8')
        html_data = f.read()
        f.close()

        self.feed(html_data)
        
        detail_start_index = self.data_list.index({'tag':['html', 'body', 'h2'],'data':'■ 상세내역'})
        only_details = map(lambda i: None if i['tag'] == ['html', 'body', 'table', 'tbody', 'tr'] else i['data'], filter(lambda data: data['tag'] == ['html', 'body', 'table', 'tbody', 'tr'] or data['tag'] == ['html', 'body', 'table', 'tbody', 'tr', 'td'], self.data_list[detail_start_index:]))
        index_order = ['이용일','이용카드','이용가맹점','이용총액','회차','할부','이번달입금하실금액_원금','이번달입금하실금액_수수료','적립예정1','적립예정2','이용혜택','혜택금액','결제후잔액','이번달입금하실금액']
        
        result = dict(unknown=[], 내역=[])

        temp_dict = dict()
        idx = 0
        for data in only_details:
            if data == None:
                if idx == len(index_order):
                    result['내역'].append(temp_dict)
                    temp_dict = dict()
                    idx = 0
                temp_dict[index_order[idx]] = ''
                idx = idx + 1
            else:
                temp_dict[index_order[idx-1]] = data
        if idx == len(index_order):
            result['내역'].append(temp_dict)
            temp_dict = dict()
            idx = 0

        return result

if __name__ == "__main__":
    if len(sys.argv) < 1:
        exit(1)

    parser = LotteCardHTMLParser()
    result = parser.parse(sys.argv[1])

    print('내역')
    for i in result['내역']:
        print(i['이용일'], i['이용가맹점'], i['이번달입금하실금액_원금'])
        pass

    exit(0)