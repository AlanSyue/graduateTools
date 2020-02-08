import json


class hcmCount(object):
    def __init__(self, lessonData, lessonCodes):
        super(hcmCount, self).__init__()
        self.lessonData = lessonData
        self.lessonCodes = lessonCodes
        self.hcmCredit = self.get_hcm_credit()
        self.generalCredit = self.get_general_credit()

    def get_hcm_credit(self):
        with open("hcm.json") as file:
            data = json.load(file)
        return data['hcm']

    def get_general_credit(self):
        with open("general.json") as file:
            data = json.load(file)
        return data['general']

    def count_hcm_credit(self):
        subjectData = self.lessonData
        subjectCodes = self.lessonCodes
        hcmCreditData = {}

        result = ''
        haveToTotal = 0
        majorTotal = 0
        optionTotal = 0
        fourChooseTwoCount = 0
        fourChooseTwoTotal = 0

        generalCredit = []

        for credit in self.hcmCredit:
            hcmCreditData.update(credit)

        for myCode in subjectCodes:
            myCode = str(myCode)
            if myCode in hcmCreditData:
                subjectType = hcmCreditData[myCode][0]['type']
                if subjectType == '0':
                    haveToTotal += 1
                elif subjectType == '1':
                    majorTotal += int(subjectData[myCode])
                elif subjectType == '2':
                    optionTotal += int(subjectData[myCode])
                elif subjectType == '3':
                    fourChooseTwoCount += 1
                    fourChooseTwoTotal += int(subjectData[myCode])
            else:
                generalCredit.append(myCode)

        if haveToTotal < 7:
            result += """
                <li>
                    <span style='color:red'>
                        軍訓、體育、社會關懷實作尚有未完成
                    </span>
                </li>
                </li><br />
            """

        result += "<li>必修學分共: " + str(majorTotal) + " 學分</li><br />"
        if majorTotal < 76:
            result += """
                <li>
                    <span style='color:red'>
                        必修尚缺 """ + str(76 - majorTotal) + """ 學分
                    </span>
                </li><br />
            """

        result += "<li>選修學分共: " + str(optionTotal) + " 學分</li><br />"
        if optionTotal < 12:
            result += """
                <li>
                    <span style='color:red'>
                        選修尚缺 """ + str(12 - optionTotal) + """ 學分</span>
                </li><br />
            """

        result += "<li>四選二學分共: " + str(fourChooseTwoTotal) + " 學分</li><br />"
        if fourChooseTwoCount < 2:
            result += """
                <li>
                    <span style='color:red'>
                        四選二尚缺 """ + str(2 - fourChooseTwoCount) + """ 門
                    </span>
                </li><br />"""

        totalCredit = majorTotal + optionTotal + fourChooseTwoTotal
        returnData = self.count_general_credit(subjectData, generalCredit)
        totalCredit = totalCredit + int(returnData[1])
        result = """
            <ul>
                <li>
                    畢業總學分為: """ + str(totalCredit) + """
                </li><br />""" + result + returnData[0]

        return result

    def count_general_credit(self, subjectData, generalCredit):
        generalCreditData = {}

        result = ''
        for credit in self.generalCredit:
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

        for myCode in generalCredit:
            myCode = str(myCode)
            if myCode in generalCreditData:

                subjectType = generalCreditData[myCode][0]['type']
                try:
                    subjectCategory = generalCreditData[myCode][0]['category']
                except KeyError:
                    pass

                if subjectType == '1':
                    if subjectCategory == '社會':
                        type1SocialCount += 1
                        type1SocialTotal += int(subjectData[myCode])
                    elif subjectCategory == '人文藝術':
                        type1ArtCount += 1
                        type1ArtTotal += int(subjectData[myCode])
                elif subjectType == '2':
                    if subjectCategory == '文學與藝術':
                        type2ArtCount += 1
                        type2ArtTotal += int(subjectData[myCode])
                    elif subjectCategory == '哲學與歷史':
                        type2HistoryCount += 1
                        type2HistoryTotal += int(subjectData[myCode])
                    elif subjectCategory == '社會科學':
                        type2SocialScienceCount += 1
                        type2SocialScienceTotal += int(subjectData[myCode])
                    elif subjectCategory == '生命科學':
                        type2BioScienceCount += 1
                        type2BioScienceTotal += int(subjectData[myCode])
                    elif subjectCategory == '物質科學與數理邏輯':
                        type2MathCount += 1
                        type2MathTotal += int(subjectData[myCode])
                    elif subjectCategory == '科技與應用':
                        type2ScienceUsedCount += 1
                        type2ScienceUsedTotal += int(subjectData[myCode])
                elif subjectType == '3':
                    if subjectCategory == '英文':
                        type3EngCount += int(subjectData[myCode])
            else:
                otherTotal += int(subjectData[myCode])

        result += """
            <li>通識-社會科學核心課程共 """ + str(type1SocialTotal) + """ 學分
            </li><br />
        """
        if type1SocialTotal < 6:
            result += """
                <li>
                    <span style='color:red'>
                        通識-社會科學核心課程尚缺 """ + str(6 - type1SocialTotal) + """ 學分
                    </span>
                </li><br />"""

        result += "<li>通識-人文藝術核心課程共 " + str(type1ArtTotal) + " 學分</li><br />"
        if type1ArtTotal < 6:
            result += """
                <li>
                    <span style='color:red'>
                        通識-人文藝術核心課程尚缺 """ + str(6 - type1SocialTotal) + """ 學分
                    </span>
                </li><br />
            """

        result += """
            <li>
                通識-英文領域共 """ + str(type3EngCount) + """ 學分
            </li><br />
        """
        if type3EngCount < 6:
            result += """
                <li>
                    <span style='color:red'>
                        通識-英文領域尚缺 """ + str(6-type3EngCount) + """ 學分
                    </span>
                </li><br />
            """

        checkType2List = [
            type2ArtCount, type2HistoryCount, type2SocialScienceCount,
            type2BioScienceCount, type2MathCount, type2ScienceUsedCount
        ]

        Type2AreaNameList = [
            '文學與藝術', '哲學與歷史', '社會科學',
            '生命科學', '物質科學與數理邏輯', '科技與應用'
        ]

        checkRun = 0  # 檢查修過幾個領域
        runCount = 0  # 檢查到第幾個領域
        passType2Area = []

        type2TotalList = [
            type2ArtTotal, type2HistoryTotal, type2SocialScienceTotal,
            type2BioScienceTotal, type2MathTotal, type2ScienceUsedTotal
        ]

        type2Total = sum(type2TotalList)
        result += "<li>通識-多元課程共 " + str(type2Total) + " 學分</li><br />"

        for type2Count in checkType2List:
            if type2Count == 0:
                checkRun += 1
            else:
                passType2Area.append(Type2AreaNameList[runCount])
            runCount += 1

        if checkRun >= 3:
            result += """
                <li>
                    通識-多元課程已修 """ + '、'.join(passType2Area) + """
                    ，<span style='color:red'>尚缺 """ + str(3 - (len(checkType2List) - checkRun)) + """ 個領域（至少選修3領域)
                    </span>
                </li><br />
        """

        result += "</ul>"

        totalList = [
            type1SocialTotal, type1ArtTotal, type3EngCount,
            type2Total, otherTotal
        ]

        generalTotalCredit = sum(totalList)
        if generalTotalCredit > 34:
            generalTotalCredit = 34

        return [result, generalTotalCredit]
