#!flask/bin/python
from flask import Flask
from flask import request
from flask import Response
import countHCM

app = Flask(__name__)


@app.route('/api/count', methods=['POST'])
def create_task():
    data = request.get_json()
    lessonData = data['data']
    lessonCodes = list(lessonData.keys())
    HCMcounter = countHCM.hcmCount(lessonData, lessonCodes)
    result = HCMcounter.count_hcm_credit()
    return Response(result, mimetype='text/plain')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
