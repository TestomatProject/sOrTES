import os
import importlib.util
from framework import Task
import sys, random, string, csv, copy
from framework import Stack

from multiprocessing import Pool

from graphviz import Digraph

from .Task import Task
from .Stack import Stack

class Handler(object):
    def run_algorithm(file_name, data_set, passed_tasks):
        algorithm = Handler.load_algorithm(file_name)

        for t in passed_tasks:
            del data_set[t]

        return algorithm(data_set).solve(passed_tasks)

    def load_algorithm(file_name):
        spec = importlib.util.spec_from_file_location(file_name.replace('/', '.'), file_name)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        class_name = file_name.split('/')[-1][:-3]

        return getattr(foo, class_name)

    def read_data_set(data_set):
        tasks = {}
        with open(data_set, 'r') as f:
            for line in f.readlines():
                data = line.strip().split(';')
                score = data[3]
                time = data[1]
                dependencies = data[2].split(',')

                if len(dependencies) == 1 and dependencies[0] == '':
                    dependencies = []

                tasks[data[0]] = Task(
                    data[0],
                    float(time),
                    float(score),
                    dependencies=dependencies
                )

        for task in tasks:
            keep_deps = []
            for dep in tasks[task].dependencies:
                keep_deps.append(tasks[dep])
                tasks[dep].add_successor(tasks[task])
            tasks[task].dependencies = keep_deps

        return tasks

    def save_data_set_plot(data_set, file_path):
        dot = Digraph(comment='Dependency Graph', format='svg')
        dot.attr(rankdir='LR', size='8,5')
        for n in data_set:
            n = data_set[n]
            rows = ['Name: ' + n._id,
                    'Time: ' + str(n.time)]
            rows.append('Score: ' + str(n.score))
            dot.node(n._id, '\n'.join(rows))

        for n1 in data_set:
            n1 = data_set[n1]
            for n2 in n1.dependencies:
                dot.edge(n2._id, n1._id)

        dot.render(filename=file_path)
