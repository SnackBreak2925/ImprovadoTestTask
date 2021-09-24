import xml.etree.ElementTree
import json
import csv
import re


def basic(raw_in):
    raw_in = sorted(raw_in, key=lambda x: x['D1'][0])
    tmpkeys = list(min(raw_in, key=len).keys())
    result = []
    for i in range(len(raw_in)):
        tmpdict = {}
        for key in raw_in[i]:
            if key in tmpkeys:
                tmpdict.update({key: raw_in[i][key]})
        result.append(dict(sorted(tmpdict.items())))
    tsv_writter = csv.DictWriter(open('basic_results.tsv', 'w', newline=''), fieldnames=tmpkeys)
    tsv_writter.writeheader()
    for i in range(len(raw_in)):
        tsv_writter.writerow(result[i])
    return result


def advanced(basic_in):
    tmp = []
    n = len(re.findall(r"[D]\d", ''.join(basic_in[0].keys())))
    for j in range(len(basic_in)):
        string = ''
        tmpm = []
        for i in range(1, n + 1):
            string += basic_in[j]['D' + str(i)]
            tmpm.append(int(basic_in[j]['M' + str(i)]))
        tmp.append([string] + tmpm)

    loopcount = len(tmp)
    i = 0
    while i < loopcount:
        j = i + 1
        while j < loopcount:
            if tmp[i][0] == tmp[j][0]:
                for k in range(1, n + 1):
                    tmp[i][k] += tmp[j][k]
                del (tmp[j])
                j -= 1
                loopcount -= 1
            j += 1
        i += 1

    advanced_solution = []
    for row in tmp:
        tmp_dict = {}
        for i in range(1, n + 1):
            tmp_dict.update({'D' + str(i): row[0][i - 1]})
        for i in range(1, n + 1):
            tmp_dict.update({'MS' + str(i): row[i]})
        advanced_solution.append(tmp_dict)

    tmpkeys = list(tmp_dict.keys())
    tsv_writter = csv.DictWriter(open('advanced_results.tsv', 'w', newline=''), fieldnames=tmpkeys)
    tsv_writter.writeheader()
    for i in range(len(advanced_solution)):
        tsv_writter.writerow(advanced_solution[i])


def readcsv(name):
    tmp_data = []
    data_csv1 = open(name, 'r')
    reader = csv.DictReader(data_csv1)
    for row in reader:
        tmp_data.append(dict(row.items()))
    return tmp_data


def readxml(name):
    root = xml.etree.ElementTree.parse(name).getroot()[0]
    tmp_xml_data = {}
    tmp_data = []
    for child in root:
        key = child.attrib['name']
        value = child[0].text
        if value.isdigit():
            value = int(value)
        tmp_xml_data.update({key: value})
    tmp_data.append(dict(tmp_xml_data.items()))
    return tmp_data


def readjson(name):
    data_json1 = json.load(open(name, 'r'))['fields']
    tmp_data = []
    for i in range(len(data_json1)):
        tmp_data.append(dict(data_json1[i].items()))
    return tmp_data


# TODO использовать аргументы командной строки при запуске сценария для подачи нескольких файлов
def main(*argv):
    # TODO запустить считывание файлов в потоках/процессах для того чтобы при обработке больших файлов ускорить процесс
    # TODO try/except для вывода ошибок без прерывания выполнения сценария
    summary = []
    summary.extend(readjson('json_data.json'))
    summary.extend(readxml('xml_data.xml'))
    summary.extend(readcsv('csv_data_1.csv'))
    summary.extend(readcsv('csv_data_2.csv'))

    advanced(basic(summary))


if __name__ == '__main__':
    main()
