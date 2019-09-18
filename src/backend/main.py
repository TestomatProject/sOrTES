from flask import Flask, request, render_template, abort, jsonify, send_file

from framework import Handler

import os, copy

app = Flask(__name__,
            static_folder = '../dist/static',
            template_folder = '../dist')

PRODUCTION = True

if not PRODUCTION:
    from flask_cors import CORS
    cors = CORS(app, resources= { r"/api/*": {"origins": "*"} })
    
ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def task_to_object(t, priority, passed_tasks):
    obj = {}
    obj['name'] = t._id
    obj['time'] = t.time
    obj['score'] = t.score
    obj['priority'] = priority
    obj['canBeExecuted'] = t.can_be_executed(passed_tasks)

    return obj

@app.route('/api/data_sets', methods=['GET', 'POST'])
def get_data_sets():
    if request.method == 'POST':
        data = request.get_json()

        if 'name' not in data or data['name'] == '' or os.path.isdir(os.path.join('data_sets', data['name'])):
            abort(403)

        os.makedirs(os.path.join('data_sets', data['name']))

        return data['name']
    else:
        data_sets = []

        for f in os.listdir('data_sets'):
            if os.path.isdir(os.path.join('data_sets', f)):
                filename = os.fsdecode(f)
                data_sets.append(filename)

        return jsonify(data_sets)

def get_data_set(name):
        data_set = {}
        data_set['name'] = name
        data_set['hasFile'] = os.path.isfile('data_sets/' + name + '/source.csv')

        return data_set

@app.route('/graphs/<name>.svg', methods=['GET'])
def get_graph(name):
    return send_file('data_sets/' + name + '/structure.svg', mimetype='image/svg+xml')

@app.route('/api/data_sets/<name>/schedule', methods=['POST'])
def schedule_of_data_set(name):
    algorithm = 'framework/algorithms/SidneyScheduler.py'

    request_data = request.get_json()
    data = Handler.read_data_set(os.path.join('data_sets/' + name, 'source.csv'))

    passed_tasks = {}
    if 'passedTests' in request_data:
        for t in request_data['passedTests']:
            passed_tasks[t] = data[t]

    schedule,time = Handler.run_algorithm(algorithm, data, copy.copy(passed_tasks))

    s = []
    priority = 1
    for t in schedule:
        s.append(task_to_object(t, priority, passed_tasks))
        priority += 1

    res = {}
    res['schedule'] = s
    res['passedTests'] = list(passed_tasks.keys())

    return jsonify(res)


@app.route('/api/data_sets/<name>', methods=['GET', 'POST', 'DELETE'])
def single_data_set(name):
    if not os.path.isdir('data_sets/' + name):
        abort(404)

    if request.method == 'POST':
        # check if the post request has the file part
        if 'source' not in request.files:
            abort(403)

        source = request.files['source']
        if source.filename == '':
            abort(403)

        if source and allowed_file(source.filename):
            source.save(os.path.join('data_sets/' + name, 'source.csv'))

            data = Handler.read_data_set(os.path.join('data_sets/' + name, 'source.csv'))
            Handler.save_data_set_plot(data, os.path.join('data_sets/' + name, 'structure'))

            return jsonify(get_data_set(name))
    elif request.method == 'DELETE':
        source_file = os.path.join('data_sets/' + name, 'source.csv')
        structure_file = os.path.join('data_sets/' + name, 'structure.svg')
        for f in [source_file, structure_file]:
            if os.path.exists(f):
                os.remove(f)

        return jsonify(get_data_set(name))
    else:
        return jsonify(get_data_set(name))


@app.route('/', defaults={ 'path': '' })
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')

if __name__ == '__main__':
    app.run(threaded=True)
