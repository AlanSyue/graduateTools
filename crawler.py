import requests
from bs4 import BeautifulSoup
import json

#########################################################################
# 用來爬取 CGU 校務資訊系統中的課程代號、學分數，並以 json 格式 儲存在 txt 文件 #
########################################################################


def subjectCralwer(url):
    domain = url
    res = requests.get(domain)
    bs = BeautifulSoup(res.text, 'html.parser')

    subjectDatas = []

    rows = bs.findAll('tr')

    subjectRow = rows

    for row in subjectRow:
        data = {}
        try:
            subjectCode = row.text.split("\n")[7]  # 課程代碼
        except NameError:
            print("no subject code")
            continue
        if subjectCode.isnumeric() is False:
            continue
        subjectName = row.text.split("\n")[13]  # 課程名稱
        data[subjectCode] = []
        data[subjectCode].append({
            "name": subjectName,
            "type": "",
        })

        subjectDatas.append(data)

    subjectDatasJson = {"ele": subjectDatas}

    with open('ele.json', 'r') as outfile:
        old_data = json.load(outfile)
        new_data = old_data['ele'] + subjectDatas
        subjectDatasJson = {"ele": new_data}

    with open('ele.json', 'w') as outfile:
        json.dump(subjectDatasJson, outfile, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    domain = "https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61"
    url_list = [
        domain + "&tabindex=1&PS=JkRQPTI3MDAmVE09NDU%3d-1tLM%2b5bk6a8%3d",
        domain + "&tabindex=1&PS=JkRQPTI3MDAmVE09NDY%3d-WD4VJrapDSk%3d",
        domain + "&tabindex=1&PS=JkRQPTI3MDAmVE09NDc%3d-euznr6hKsfQ%3d",
        domain + "&tabindex=1&PS=JkRQPTI3MDAmVE09NDg%3d-RX27F34c9bM%3d",
        domain + "&tabindex=1&PS=JkRQPTI3MDAmVE09NDk%3d-cOzl4KHl2xM%3d",
        domain + "&tabindex=1&PS=JkRQPTI3MDAmVE09NTA%3d-wNYnIB9lwMM%3d",
        domain + "&tabindex=1&PS=JkRQPTI3MDAmVE09NTE%3d-z4nK62dbMoc%3d",
        domain + "&tabindex=1&PS=JkRQPTI3MDAmVE09NTI%3d-NknlkDjAhSE%3d"
    ]

    for url in url_list:
        print("========start======" + url + "==============")
        subjectCralwer(url)
        print("========end=================================")
