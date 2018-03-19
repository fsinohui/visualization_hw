from flask import Flask, render_template, jsonify
from database import otuOutput, nameOutput, washFreq, metaOutput, sampleJson, sampleJsonAll

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/v1/otu')
def otu():
    otuOutputList = otuOutput()
    return (jsonify(otuOutputList))


@app.route('/api/v1/names')
def names():
    sampleNameList = nameOutput()
    return (jsonify(sampleNameList))


@app.route('/api/v1/wfreq/<sample>')
def wfreq(sample):
    washOutputList = washFreq(sample)
    return jsonify(washOutputList)


@app.route('/api/v1/metadata/<sample>')
def meta(sample):
    dataDict = metaOutput(sample)
    return jsonify(dataDict)


@app.route('/api/v1/samples/<sample>')
def sampleSample(sample):
    dataDict = sampleJson(sample)
    return jsonify(dataDict)


@app.route('/api/v1/samplesall/<sample>')
def sampleSampleAll(sample):
    dataDict = sampleJsonAll(sample)
    return jsonify(dataDict)


if __name__ == '__main__':
    app.run(debug=True)