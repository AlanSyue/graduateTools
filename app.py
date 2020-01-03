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
	lessonData = data['data']
	lessonCodes = list(lessonData.keys())

	result = count_hcm_credit(lessonData, lessonCodes)
	
	return Response(result, mimetype='text/plain')

def count_hcm_credit(subjectData, subjectCodes):
	hcmCredit = get_hcm_credit()
	hcmCreditData = {}

	result = ''
	haveToTotal = 0
	majorTotal = 0
	optionTotal = 0
	fourChooseTwoCount = 0
	fourChooseTwoTotal = 0

	generalSubjectCredit = []

	for credit in hcmCredit:
		hcmCreditData.update(credit)

	for mySubjectCode in subjectCodes:
		mySubjectCode = str(mySubjectCode)
		if mySubjectCode in hcmCreditData:
			subjectType = hcmCreditData[mySubjectCode][0]['type']
			if subjectType == '0':
				haveToTotal+=1
			elif subjectType == '1':
				majorTotal += int(subjectData[mySubjectCode])
			elif subjectType == '2':
				optionTotal += int(subjectData[mySubjectCode])
			elif subjectType == '3':
				fourChooseTwoCount +=0
				fourChooseTwoTotal += int(subjectData[mySubjectCode])
		else:
			generalSubjectCredit.append(mySubjectCode)

	if haveToTotal < 7:
		result += "<li><span style='color:red'>軍訓、體育、社會關懷實作尚有未完成</span></li></li><br />"

	result += "<li>必修學分共: " + str(majorTotal) + " 學分</li><br />"
	if majorTotal < 76:
		result += "<li><span style='color:red'>必修尚缺 " + str( 76 - majorTotal ) + " 學分</span></li><br />"

	result += "<li>選修學分共: " + str(optionTotal) + " 學分</li><br />"
	if optionTotal < 12:
		result += "<li><span style='color:red'>選修尚缺 " + str( 12 - optionTotal ) + " 學分</span></li><br />"

	result += "<li>四選二學分共: " + str(fourChooseTwoTotal) + " 學分</li><br />"
	if fourChooseTwoCount < 2:
		result += "<li><span style='color:red'>四選二尚缺 " + str(2 - fourChooseTwoCount) + " 門</span></li><br />"

	totalCredit = majorTotal + optionTotal + fourChooseTwoTotal
	returnData = count_general_credit(subjectData, generalSubjectCredit)
	totalCredit = totalCredit + int(returnData[1])
	result = '<ul><li>畢業總學分為: ' + str(totalCredit) + " </li><br />" + result + returnData[0];

	return result

def count_general_credit(subjectData, generalSubjectCredit):
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

	type2ScienceUsedCount = 0
	type2ScienceUsedTotal = 0

	type3EngCount = 0
	otherTotal = 0
	
	for mySubjectCode in generalSubjectCredit:
		mySubjectCode = str(mySubjectCode)
		if mySubjectCode in generalCreditData:

			subjectType = generalCreditData[mySubjectCode][0]['type']
			try:
				subjectCategory = generalCreditData[mySubjectCode][0]['category']
			except:
				pass

			if subjectType == '1':
				if subjectCategory == '社會':
					type1SocialCount += 1
					type1SocialTotal += int(subjectData[mySubjectCode])
				elif subjectCategory == '人文藝術':
					type1ArtCount += 1
					type1ArtTotal += int(subjectData[mySubjectCode])	
			elif subjectType == '2':
				if subjectCategory == '文學與藝術':
					type2ArtCount += 1
					type2ArtTotal += int(subjectData[mySubjectCode])
				elif subjectCategory == '哲學與歷史':
					type2HistoryCount += 1
					type2HistoryTotal += int(subjectData[mySubjectCode])
				elif subjectCategory == '社會科學':
					type2SocialScienceCount += 1
					type2SocialScienceTotal += int(subjectData[mySubjectCode])
				elif subjectCategory == '生命科學':
					type2BioScienceCount += 1
					type2BioScienceTotal += int(subjectData[mySubjectCode])
				elif subjectCategory == '物質科學與數理邏輯':
					type2MathCount += 1
					type2MathTotal += int(subjectData[mySubjectCode])
				elif subjectCategory == '科技與應用':
					type2ScienceUsedCount += 1
					type2ScienceUsedTotal += int(subjectData[mySubjectCode])
			elif subjectType == '3':
				if subjectCategory == '英文':
					type3EngCount += int(subjectData[mySubjectCode])
		else:
			otherTotal += int(subjectData[mySubjectCode])

	result += "<li>通識-社會科學核心課程共 " + str( type1SocialTotal ) + " 學分</li><br />"
	if type1SocialTotal < 6:
		result += "<li><span style='color:red'>通識-社會科學核心課程尚缺 " + str( 6 - type1SocialTotal ) + " 學分</span></li><br />"

	result += "<li>通識-人文藝術核心課程共 " + str( type1ArtTotal ) + " 學分</li><br />"
	if type1ArtTotal < 6:
		result += "<li><span style='color:red'>通識-人文藝術核心課程尚缺 " + str( 6 - type1SocialTotal ) + " 學分</span></li><br />"

	result += "<li>通識-英文領域共 " + str( type3EngCount ) + " 學分</li><br />"
	if type3EngCount < 6:
		result += "<li><span style='color:red'>通識-英文領域尚缺 " + str(6-type3EngCount) + " 學分</span></li><br />"

	checkType2List = [
		type2ArtCount, type2HistoryCount, type2SocialScienceCount,
		type2BioScienceCount, type2MathCount, type2ScienceUsedCount
	]

	Type2AreaNameList = [
		'文學與藝術', '哲學與歷史', '社會科學',
		'生命科學', '物質科學與數理邏輯', '科技與應用'
	]

	checkRun = 0 # 檢查修過幾個領域
	runCount = 0 # 檢查到第幾個領域
	passType2Area = []
	type2Total = type2ArtTotal + type2HistoryTotal + type2SocialScienceTotal + type2BioScienceTotal + type2MathTotal + type2ScienceUsedTotal
	result += "<li>通識-多元課程共 " + str( type2Total ) + " 學分</li><br />"

	for type2Count in checkType2List:
		if type2Count == 0:
			checkRun += 1
		else:
			passType2Area.append(Type2AreaNameList[runCount]) 
		runCount += 1

	if checkRun >= 3:
		result += "<li>通識-多元課程已修 " + '、'.join(passType2Area) + "，<span style='color:red'>尚缺 " + str( 3 - ( len(checkType2List) - checkRun )) + " 個領域（至少選修3領域)</span></li><br />"
	
	result += "</ul>"
	generalTotalCredit = type1SocialTotal + type1ArtTotal + type3EngCount + type2Total + otherTotal
	if generalTotalCredit > 34:
		generalTotalCredit = 34

	return [result, generalTotalCredit]

if __name__ == '__main__':
    app.run(debug=True)

