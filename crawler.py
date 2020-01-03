import requests
from bs4 import BeautifulSoup
import json
import sys

#########################################################################
# 用來爬取 CGU 校務資訊系統中的課程代號、學分數，並以 json 格式 儲存在 txt 文件 #
########################################################################
def subjectCralwer(url):
	domain = url
	cookie = {"Cookie": Cookie}
	res = requests.post(domain, cookies=cookie)
	bs = BeautifulSoup(res.text,'html.parser')

	subjectDatas = []

	rows = bs.findAll('tr')

	subjectRow = rows

	for row in subjectRow:
		data = {}
		try:
			subjectCode = row.text.split("\n")[7] #課程代碼
		except:
			continue
		if subjectCode.isnumeric() == False:
			continue
		subjectName = row.text.split("\n")[13] #課程名稱
		data[subjectCode] = []
		data[subjectCode].append({
			"name" : subjectName,
			"type" : "",
			"category": "" ,
		})

		subjectDatas.append(data)

	subjectDatasJson = {"general" : subjectDatas}

	with open('general_v2.txt', 'r') as outfile:
		old_data = json.load(outfile)
		new_data = old_data['general'] + subjectDatas
		subjectDatasJson = {"general" : new_data}

	with open('general_v2.txt', 'w') as outfile:
	    json.dump(subjectDatasJson, outfile, ensure_ascii=False, indent=2)

if __name__ == '__main__':
	url_list = [
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09MjY%3d-iMYkGd8uP8E%3d',
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09Mjc%3d-0Bt%2badHTyyA%3d',
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09Mjg%3d-TWf%2fzImJ2m4%3d',
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09Mjk%3d-lCYRXfCM0ks%3d',
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09MzA%3d-11tHvBf2pCw%3d',
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09MzE%3d-0YC0xW3KTd4%3d',
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09MzI%3d-xIqsbXc99qc%3d',
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09MzM%3d-h7LPpkLZH9k%3d',
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09MzQ%3d-cMDgVWNuit0%3d',
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09MzU%3d-sCNndpSsFzc%3d',
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09MzY%3d-MHmt6qIBXgY%3d',
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09Mzc%3d-IUlRh%2fY7v4Q%3d',
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09Mzg%3d-abhn6QkqhUc%3d',
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09Mzk%3d-hsOIHgUvon8%3d',
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09NDA%3d-U4LUrNs9Rl0%3d',
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09NDE%3d-zY2W%2flwkLoA%3d',
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09NDI%3d-aAVFaFwnLb0%3d',
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09NDM%3d-4sCh7mzab3A%3d',
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09NDQ%3d-Qwmooh1jnnI%3d',
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09NDU%3d-FOh0UmLCfdQ%3d',
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09NDY%3d-ifSLBw%2b9J8c%3d',
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09NDg%3d-U2OD0LzPKA8%3d',
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09NDk%3d-JFJOs0Yq8cA%3d',
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09NTE%3d-otw8Cque3m0%3d',
		'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09NTI%3d-O5MAa6YvJ34%3d'
	]

	for url in url_list:
		print("========start======" +url + "==============")
		subjectCralwer(url)
		print("========end=================================")