import xlrd
import sys
import re

def parse(file_path):
    worksheet = xlrd.open_workbook(file_path).sheet_by_index(0)
    
    result = dict(unknown=[], 내역=[])
    for row in worksheet.get_rows():
        row_dict = dict(
            이용일자                      =   row[1].value.replace('\xa0', ''),
            이용카드                      =   row[2].value.replace('\xa0', ''),
            구분                          =   row[3].value.replace('\xa0', ''),
            이용하신가맹점                 =   row[4].value.replace('\xa0', ''),
            #    =   row[5].value,
            이용금액                       =   row[6].value.replace('\xa0', ''),
            할부개월                       =   row[7].value.replace('\xa0', ''),
            이번달결제금액_회차             =   row[8].value.replace('\xa0', ''),
            이번달결제금액_원금             =   row[9].value.replace('\xa0', ''),
            이번달결제금액_수수료_이자      =   row[10].value.replace('\xa0', ''),
            결제후잔액_회차                =   row[11].value.replace('\xa0', ''),
            결제후잔액_원금                =   row[12].value.replace('\xa0', ''),
            적립예정포인트                 =   row[13].value.replace('\xa0', ''),
        )
        
        if re.match('\d{2}.\d{2}.\d{2}', row_dict['이용일자']):
            result['내역'].append(row_dict)
        else:
            result['unknown'].append(row_dict)
    return result

if __name__ == "__main__":
    if len(sys.argv) < 1:
        exit(1)

    result = parse(sys.argv[1])
    print('내역')
    for i in result['내역']:
        print(i['이용일자'], i['이용하신가맹점'], i['이용금액'], i['이번달결제금액_원금'], i['결제후잔액_원금'])
        pass
    
    print('unknown')
    for i in result['unknown']:
        print(i['이용일자'], i['이용하신가맹점'], i['이용금액'], i['이번달결제금액_원금'], i['결제후잔액_원금'])
        pass
    exit(0)