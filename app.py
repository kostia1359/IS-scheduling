import json
import hashlib

from flask import Flask, render_template, jsonify, Response, request
from models import DataManager
from scheduling import Scheduler

app = Flask(__name__)

scheduler = Scheduler()

@app.route('/')
def index():
    return render_template('schedule.html')


@app.route('/database')
def database():
    return render_template('data.html')


@app.route('/database/<data>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_data(data):
    if request.method == 'GET':
        return Response(json.dumps(DataManager.get_data(data), ensure_ascii=False), mimetype='application/json')
    elif request.method == 'POST' or request.method == 'PUT':
        DataManager.create(data, request.form)
        return ''
    else:
        DataManager.delete(data, request.form['id'])
        return ''


@app.route("/schedule")
def get_schedule():
    return Response(json.dumps(scheduler.generate(), ensure_ascii=False), mimetype='application/json')


if __name__ == '__main__':
    app.run()
