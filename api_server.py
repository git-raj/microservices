#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 17:53:09 2018

@author: Saroj Lamichhane
"""

#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
import json


app = Flask(__name__)

def read_file():
    with open('datafile.json', 'r') as f:
        tasks = json.load(f)
    return tasks

def append_to_file(task):
    with open('datafile.json', 'w') as f:
        json.dump(task, f)

#
#def load_to_file(task):
#    with open('file.json', 'w') as f:
#        json.dump(task, f)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not Found'}), 404)

#get all tasks
@app.route('/myapp/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    tasks = read_file()
    return jsonify({'tasks': tasks})


@app.route('/myapp/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    tasks = read_file()
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task':task[0]})

@app.route('/myapp/api/v1.0/tasks/', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    tasks = read_file()
    task = {"id":tasks[-1]['id']+1,
            "title": request.json['title'],
            "description": request.json.get('description', ""),
            "done": False}
    append_to_file(task)


@app.route('/myapp/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = read_file()
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    append_to_file(tasks)
    return jsonify({'result':True})


@app.route('/')
def index():
    return "Home."

if __name__ == "__main__":
    app.run(debug=True)
