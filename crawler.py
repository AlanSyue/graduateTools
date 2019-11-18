import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import sys


def test():
	domain = 'https://ep.cgu.edu.tw/webfolio/progression_1.aspx?um_id=200&RNO=14351'
	data = {
		"Cookie":"ZNPCQ003-32303500=0840f49f; _ga=GA1.3.122716898.1569113838; ZNPCQ003-32323200=936fad10; ZNPCQ003-36393300=23cfc60a; ZNPCQ003-32353300=d3d7fe70; ZNPCQ003-31303600=8ef8d53e; ASP.NET_SessionId=shxsul5lprkfarcg0zaarmnx; ZNPCQ003-31333200=b269cecf; _gid=GA1.3.1995999088.1571753933; userInfo=76C399BC4FE46D854D5B07F9E1707CEA687DC3DE2D9BC8E0261B9C35DC0AED6DDE4E6244FF7D76EE8F2AA759D8CED785F3BAAC4E725249CA0F4E1454111AF3DF1FB7BD84F5432EACB7DC50CCDBF22AE9EB13B8F56D2905AAA185182F1894449748C2FE8EF66DC5997C61F2446E71F35938575F0AE08365B2510CC4E3A317C5A2B344517A480E4402C6952CF821FF5EF433A00850E2BDC7368D0CE6134E17C2BE45FA4AB49066CDF62C575271A6B34CC9C13E4BA49119E4710D169725593FAC039055FD014D3002840EDE868721FCFBCF8D95EC0A79E574D8FAF387B4D2FF18F886BADB3C8BE6E70312C2BE2EEAB97E4CF653CF1D337D6E3EC6830BF4B4931986734731A17ED0CB4CD9E3A69C559E3C598CD1C136EC695E6D4ACB49F525231269C8C19520CC65F29E15DB3EE426E9E5D9A9F67F1B; _gat=1; _gat_gtag_UA_125435851_1=1; ASPSESSIONIDSCBTDBSA=EBNNBGDAKOALPMMMINANNJBE"
	}	
	# 將資料加入 POST 請求中
	res = requests.post(domain, cookies=data)
	bs = BeautifulSoup(res.text,'html.parser')

	tr = bs.findAll('tr')
	count =0
	for row in tr:
		code = row.text.split("\n")[1]
		print(code)
		if code.isnumeric():
			print(code)
			count+=1
	print('total'+str(count))

#########################################################################
# 用來爬取 CGU 校務資訊系統中的課程代號、學分數，並以 json 格式 儲存在 txt 文件 #
########################################################################
def subjectCralwer(url):
	domain = url
	cookie = {"Cookie":"ZNPCQ003-32303500=0840f49f; _ga=GA1.3.122716898.1569113838; ZNPCQ003-32323200=936fad10; ZNPCQ003-36393300=23cfc60a; ZNPCQ003-32353300=d3d7fe70; ZNPCQ003-31303600=8ef8d53e; ZNPCQ003-31333200=b269cecf; _gid=GA1.3.15780854.1571412306; IPCZQX0339d3a182=01002700c0a8ba97be0ad253ed27278c9c922ccf; .ASPXAUTH=398F7E486B15458A318C936038B98905F08253BDC9B1113D698F3CF697496275489BA58C24B0E516B712D8A770253B24E06C6182750343CD46D6DC1C2F313B74A05D43F0A850CA493A0319F76DA837479BD8628F202983D26FA766130735D8D1BED8403E075AEF65B5F5389438703A2D6DC7B94B; userInfo=FCDCAECC31C7744D62BC1A272B0B63147D8F7A0458E4FA6EA4E36709AFF27DBB8F39ED2047E262817E24477DCEECD971B0F6E96F729A294805EF593909C85B2DE2EF836260ADEBFA1BBC126063EB0009514B232D288B36AA3C3F5D7CC6AD99D42B53E91D3CA007D4FD7864835DE4270482F1E7ACAEF847C33F5632D8DB39C441FCBE9A8DF3D560CA76C75A238E2ED93EAD2602074E7F813126F77FBF2F76105375D824CFEDF465D8BFE566142C7A30F84DA2117BFF6BF44D578AA51A8B5C5A4F88459C18B44F207BB0B7756CE4FA20CCE5F2A55FCBC2393042FD6D2B40A7AAB3E1B682C7577703AD8616E3841BFE0E3B65621F21108552C46A2AFC5A1F6086DC2A0AEB53CBD58793ABB770AFE4104E35B8FAF55743F4115F926EDE49EE25A50DE01B42004FEA73284C26B9724D71E22E3321094E"}
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
		subjectCredit = row.text.split("\n")[21].split("\r")[0] #學分數

		data[subjectCode] = []
		data[subjectCode].append({
			"name" : subjectName,
			"type" : "",
			"credit" : subjectCredit
		})

		subjectDatas.append(data)

	#subjectDatasJson = {"general" : subjectDatas}

	# with open('general.txt', 'w') as outfile:
	# 	json.dump(subjectDatasJson, outfile,ensure_ascii=False,indent=2)
	# exit()

	with open('general.txt', 'r') as outfile:
	    old_data = json.load(outfile)
	    new_data = old_data['general'] + subjectDatas
	    subjectDatasJson = {"general" : new_data}

	with open('general.txt', 'w') as outfile:
	    json.dump(subjectDatasJson, outfile, ensure_ascii=False, indent=2)

if __name__ == '__main__':
	test()
	# url_list = [
	# 	'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09MjY%3d-iMYkGd8uP8E%3d',
	# 	'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09Mjc%3d-0Bt%2badHTyyA%3d',
	# 	'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09Mjg%3d-TWf%2fzImJ2m4%3d',
	# 	'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09Mjk%3d-lCYRXfCM0ks%3d',
	# 	'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09MzA%3d-11tHvBf2pCw%3d',
	# 	'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09MzE%3d-0YC0xW3KTd4%3d',
	# 	'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09MzI%3d-xIqsbXc99qc%3d',
	# 	'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09MzM%3d-h7LPpkLZH9k%3d',
	# 	'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09MzQ%3d-cMDgVWNuit0%3d',
	# 	'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09MzU%3d-sCNndpSsFzc%3d',
	# 	'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09MzY%3d-MHmt6qIBXgY%3d',
	# 	'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09Mzc%3d-IUlRh%2fY7v4Q%3d',
	# 	'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09Mzg%3d-abhn6QkqhUc%3d',
	# 	'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09Mzk%3d-hsOIHgUvon8%3d',
	# 	'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09NDA%3d-U4LUrNs9Rl0%3d',
	# 	'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09NDE%3d-zY2W%2flwkLoA%3d',
	# 	'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09NDI%3d-aAVFaFwnLb0%3d',
	# 	'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09NDM%3d-4sCh7mzab3A%3d',
	# 	'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09NDQ%3d-Qwmooh1jnnI%3d',
	# 	'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09NDU%3d-FOh0UmLCfdQ%3d',
	# 	'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09NDY%3d-ifSLBw%2b9J8c%3d',
	# 	'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09NDg%3d-U2OD0LzPKA8%3d',
	# 	'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09NDk%3d-JFJOs0Yq8cA%3d',
	# 	'https://www.is.cgu.edu.tw/portal/DesktopDefault.aspx?tabid=61&tabindex=1&PS=JkRQPTUwMDAmVE09NTE%3d-otw8Cque3m0%3d'
	# ]

	# for url in url_list:
	# 	subjectCralwer(url)
	# with open('general.txt') as json_file:
	#     data = json.load(json_file)
	#     print(data)