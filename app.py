#!flask/bin/python
from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
import requests
from bs4 import BeautifulSoup
import json

def get_hcm_credit():
	with open("hcm.txt") as file:
		data = json.load(file)
	return data['hcm']

def get_general_credit():
	with open("general.txt") as file:
		data = json.load(file)
	return data['general']

app = Flask(__name__)

@app.route('/api/count', methods=['POST'])
def create_task():
	data = request.get_json()

	subjectCodeArray = []

	domain_list = [
		"https://ep.cgu.edu.tw/webfolio/progression_1.aspx?RC_Level=1&RC_Semester=U",
		"https://ep.cgu.edu.tw/webfolio/progression_1.aspx?RC_Level=1&RC_Semester=D",
		"https://ep.cgu.edu.tw/webfolio/progression_1.aspx?RC_Level=2&RC_Semester=U",
		"https://ep.cgu.edu.tw/webfolio/progression_1.aspx?RC_Level=2&RC_Semester=D",
		"https://ep.cgu.edu.tw/webfolio/progression_1.aspx?RC_Level=2&RC_Semester=S",
		"https://ep.cgu.edu.tw/webfolio/progression_1.aspx?RC_Level=3&RC_Semester=U",
		"https://ep.cgu.edu.tw/webfolio/progression_1.aspx?RC_Level=3&RC_Semester=D",
		"https://ep.cgu.edu.tw/webfolio/progression_1.aspx?RC_Level=3&RC_Semester=S",
		"https://ep.cgu.edu.tw/webfolio/progression_1.aspx?RC_Level=4&RC_Semester=U",
		"https://ep.cgu.edu.tw/webfolio/progression_1.aspx?RC_Level=4&RC_Semester=D",
	]

	for domain in domain_list:
		#將資料加入 POST 請求中
		res = requests.post(domain, cookies = {'Cookie':data['Cookie']})
		bs = BeautifulSoup(res.text,'html.parser')
		h1 = bs.find('h1').text
		trs = bs.findAll('tr')
		for row in trs:
			code = row.text.split("\n")[1]
			if code.isnumeric():
				score = row.text.split("\n")[4]
				if score.isnumeric():
					if int(score) >= 60:
						subjectCodeArray.append(code)

	result = count_hcm_credit(subjectCodeArray)
	
	return Response(result, mimetype='text/plain')

def count_hcm_credit(subjectCodes):
	hcmCredit = get_hcm_credit()
	hcmCreditData = {}

	result = '<ul>'
	haveToTotal = 0
	majorTotal = 0
	optionTotal = 0
	fourChooseTwoCount = 0
	fourChooseTwoTotal = 0

	generalSubjectCredit = []

	for credit in hcmCredit:
		hcmCreditData.update(credit)

	for mySubjectCode in subjectCodes:
		if mySubjectCode in hcmCreditData:
			subjectType = hcmCreditData[mySubjectCode][0]['type']
			subjectCredit = int(hcmCreditData[mySubjectCode][0]['credit'])
			if subjectType == '0':
				haveToTotal+=1
			elif subjectType == '1':
				majorTotal += subjectCredit
			elif subjectType == '2':
				optionTotal += subjectCredit
			elif subjectType == '3':
				fourChooseTwoCount +=0
		else:
			generalSubjectCredit.append(mySubjectCode)

	if haveToTotal < 7:
		result += "<li>軍訓、體育、社會關懷實作尚有未完成</li></li><br />"
	if majorTotal < 76:
		result += "<li>必修尚缺" + str(majorTotal - 76) + " 學分</li><br />"
	if optionTotal < 12:
		result += "<li>選修尚缺 " + str(optionTotal - 12) + " 學分</li><br />"
	if fourChooseTwoCount < 2:
		result += "<li>四選二尚缺 " + str(2 - fourChooseTwoCount) + " 門</li><br />"

	result += count_general_credit(generalSubjectCredit)

	return result

def count_general_credit(generalSubjectCredit):
	generalCredit = get_general_credit()
	generalCreditData = {}

	result = ''
	for credit in generalCredit:
		generalCreditData.update(credit)

	type1SocialCount = 0
	type1SocialTotal = 0

	type1ArtCount = 0
	type1ArtTotal = 0

	type2ArtCount = 0
	type2ArtTotal = 0

	type2HistoryCount = 0
	type2HistoryTotal = 0

	type2SocialScienceCount = 0
	type2SocialScienceTotal = 0

	type2BioScienceCount = 0
	type2BioScienceTotal = 0

	type2MathCount = 0
	type2MathTotal = 0

	type3EngCount = 0
	otherTotal = 0
	
	for mySubjectCode in generalSubjectCredit:
		if mySubjectCode in generalCreditData:

			subjectType = generalCreditData[mySubjectCode][0]['type']
			try:
				subjectCategory = generalCreditData[mySubjectCode][0]['category']
			except:
				pass
			subjectCredit = int(generalCreditData[mySubjectCode][0]['credit'])

			if subjectType == '1':
				if subjectCategory == '社會':
					type1SocialCount += 1
					type1SocialTotal += subjectCredit
				elif subjectCategory == '人文藝術':
					type1ArtCount += 1
					type1ArtTotal += subjectCredit	
			elif subjectType == '2':
				if subjectCategory == '文學與藝術':
					type2ArtCount += 1
					type2ArtTotal += subjectCredit
				elif subjectCategory == '哲學與歷史':
					type2HistoryCount += 1
					type2HistoryTotal += subjectCredit
				elif subjectCategory == '社會科學':
					type2SocialScienceCount += 1
					type2SocialScienceTotal += subjectCredit
				elif subjectCategory == '生命科學':
					type2BioScienceCount += 1
					type2BioScienceTotal += subjectCredit
				elif subjectCategory == '物質科學與數理邏輯':
					type2MathCount += 1
					type2MathTotal += subjectCredit
			elif subjectType == '3':
				if subjectCategory == '英文':
					type3EngCount += subjectCredit
			else:
				otherTotal += subjectCredit

	if type1SocialTotal < 6:
		result += "<li>通識-社會科學核心課程尚缺 " + str(6-type1SocialTotal) + " 學分</li><br />"
	if type1ArtTotal < 6:
		result += "<li>通識-人文藝術核心課程尚缺 " + str(6-type1SocialTotal) + " 學分</li><br />"
	if type3EngCount < 6:
		result += "<li>通識-英文領域尚缺 " + str(6-type3EngCount) + " 學分</li><br />"

	checkType2List = [
		type2ArtCount, type2HistoryCount, type2SocialScienceCount,
		type2BioScienceCount, type2MathCount
	]

	checkRun = 0
	for type2Count in checkType2List:
		if type2Count == 0:
			checkRun+=1
	if checkRun >=3:
		result += "<li>通識-多元課程尚缺 " + str(3 - ( 5- checkRun )) + " 個領域（至少選修 3 領域)</li><br />" 

	result += "</ul>"
	return result

if __name__ == '__main__':
    app.run(debug=True)

