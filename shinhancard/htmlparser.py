from html.parser import HTMLParser
import copy
import sys

class ShinhanCardHTMLParser(HTMLParser):
    data_list = []
    full_tag = []

    def handle_starttag(self, tag, attrs):
        self.full_tag.append(tag)

    def handle_endtag(self, tag):
        self.full_tag.pop()

    def handle_data(self, data):
        data = data.strip()
        self.data_list.append({'tag':copy.deepcopy(self.full_tag), 'data':data})
    
    def parse(self, filepath):
        f = open(filepath, 'r', encoding='EUC-KR')
        html_data = f.read()
        f.close()

        self.feed(html_data)

        # {'tag': ['html', 'head', 'title'], 'data': '체크카드 이메일명세서'}, 
        title = list(filter(lambda data: data['tag'] == ['html', 'head', 'title'], self.data_list))[0]['data']
        if '체크카드 이메일명세서' == title:
            # {'tag': ['html', 'body', 'div', 'div', 'div', 'table', 'tbody', 'tr', 'td'], 'data': '성남사랑 신한카드 chak Deep Dream(체크)'},
            ################
            # {'tag': ['html', 'body', 'div', 'div', 'div', 'h3'], 'data': '카드이용내역'}, 
            # {'tag': ['html', 'body', 'div', 'div', 'div', 'table', 'thead', 'tbody', 'tr', 'td'], 'data': '21.07.20'}, 
            detail_start_index = self.data_list.index({'tag': ['html', 'body', 'div', 'div', 'div', 'h3'], 'data': '카드이용내역'})
            only_details = map(lambda i: i['data'], filter(lambda data: data['tag'] == ['html', 'body', 'div', 'div', 'div', 'table', 'thead', 'tbody', 'tr', 'td'], self.data_list[detail_start_index:]))
            index_order = ['이용일자','이용카드','이용카드번호','이용가맹점','이용금액_이용원금','이용금액_수수료','이용금액_할인금액','이용금액_입금완납금액','입금하실금액','캐시백','포인트적립율(마이신한)']
        elif '이메일명세서'  == title:
            detail_start_index = self.data_list.index({'tag': ['html', 'body', 'div', 'div', 'div', 'h3'], 'data': '카드이용내역'})
            only_details = map(lambda i: i['data'], filter(lambda data: data['tag'] == ['html', 'body', 'div', 'div', 'div', 'table', 'thead', 'tbody', 'tr', 'td']
                                                           or data['tag'] ==  ['html', 'body', 'div', 'div', 'div', 'table', 'thead', 'tbody', 'tr', 'td', 'a']
                                                           , self.data_list[detail_start_index:]))
            index_order = ['이용일자','이용카드','이용카드번호','이용가맹점','이용금액','할부기간/회차','이번달내실금액_원금','이번달내실금액_수수료(이자)','할인/면제P사용_구분','할인/면제/P사용_금액','결제후잔액','포인트적립율(마이신한)']

        result = dict(unknown=[], 내역=[])

        temp_dict = dict()
        idx = 0
        for data in only_details:
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

    parser = ShinhanCardHTMLParser()
    result = parser.parse(sys.argv[1])

    print('내역')
    for i in result['내역']:
        print(i['이용일자'], i['이용가맹점'],  i['이번달내실금액_원금'] if '이번달내실금액_원금' in i else i['이용금액_이용원금'])
        pass

    exit(0)