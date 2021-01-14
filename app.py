from flask import Flask
from flask import render_template, request, flash, redirect, url_for
from GA import run
from gevent import pywsgi
import re

app = Flask(__name__)
app.secret_key = '32916abafe7f9cc15e6c336cbcf07831'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/random')
def random():
    run.runGA()
    filename = run.drawScatter()
    resultData = run.getData()
    # for i in range(len(resultData)):
    #     for j in range(len(resultData[i])):
    #         resultData[i][j] = round(resultData[i][j], 1)
    return render_template('random.html', filename=filename)


@app.route('/parameter', methods=['GET', 'POST'])
def parameter():
    if request.form.get('start', None):
        userConfig = {}
        userConfig['taskNum'] = request.form['taskNum']
        userConfig['nodeNum'] = request.form['nodeNum']
        userConfig['iteratorNum'] = request.form['iteratorNum']
        userConfig['chromosomeNum'] = request.form['chromosomeNum']
        userConfig['cp'] = request.form['cp']
        parameter_empty = 0
        # print(userConfig)
        for i in userConfig.values():
            if is_number(i) == False:
                flash(u'参数错误')
                return redirect(url_for('parameter'))
        run.runGA(userConfig=userConfig)
        filename = run.drawScatter()
        return render_template('parameter.html', parameter_empty=parameter_empty, filename=filename, userConfig=userConfig)
    else:
        parameter_empty = 1
        return render_template('parameter.html', parameter_empty=parameter_empty)


def is_number(num):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(num)
    if result:
        return True
    else:
        return False


if __name__ == '__main__':
    # app.run()
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()
