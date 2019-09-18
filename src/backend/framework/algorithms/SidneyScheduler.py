from igraph import Graph

import copy, time, math

class SidneyScheduler(object):
    def __init__(self, tasks, precision = 2):
        self.tasks_dict = tasks
        self.tasks = list(tasks.values())
        self.precision = precision

    def get_capacity(source, to, source_task, to_task, lamb):
        if source == 'DummyStart':
            return lamb * to_task.score
        elif to == 'DummyEnd':
            return source_task.time
        else:
            return math.inf


    def get_next_tasks(self, tasks_to_be_scheduled, lamb_min):
        if len(tasks_to_be_scheduled) == 1:
            return [ list(tasks_to_be_scheduled.values())[0] ], lamb_min

        # Add edges
        sum_of_score = 0
        for t in tasks_to_be_scheduled:
            t = tasks_to_be_scheduled[t]
            sum_of_score += t.score

        lamb_max = lamb_min + sum_of_score * 2
        lamb_bound = lamb_max
        cut = []
        lamb_old = 0
        while True:
            lamb = 0.5 * (lamb_max + lamb_min)

            capacities = []
            i = 0

            for e in self.graph.es:
                source = self.graph.vs[e.source]['name']
                target = self.graph.vs[e.target]['name']

                if source != 'DummyStart' and source != 'DummyEnd':
                    source_node = tasks_to_be_scheduled[source]
                else:
                    source_node = None

                if target != 'DummyStart' and target != 'DummyEnd':
                    target_node = tasks_to_be_scheduled[target]
                else:
                    target_node = None

                capacities.append(SidneyScheduler.get_capacity(source, target, source_node, target_node, lamb))

            self.graph.es['capacity'] = capacities

            cut = self.graph.st_mincut(len(tasks_to_be_scheduled), len(tasks_to_be_scheduled) + 1, 'capacity')

            value_is_accepted = lamb * sum_of_score >= cut.value
            cut_contains_tasks = len(cut[0]) > 1
            movement = math.fabs(lamb_old - lamb)
            lamb_old = lamb
            movement_is_small = movement < self.precision

            if value_is_accepted and cut_contains_tasks and movement_is_small:
                break
            else:
                if cut_contains_tasks and value_is_accepted:
                    lamb_max = lamb
                else:
                    lamb_min = lamb

                    if lamb_max - lamb_min < self.precision:
                        lamb_max += self.precision

                        if lamb_max > lamb_bound:
                            cut = (range(0,len(tasks_to_be_scheduled)), [])
                            break

        tasks = []
        for c in cut[0]:
            if c < len(tasks_to_be_scheduled):
                tasks.append(tasks_to_be_scheduled[self.graph.vs[c]['name']])

        return tasks,lamb

    def greedy_solve(tasks, passed_tasks):
        schedule = []

        tasks = sorted(tasks, key=lambda x: x.score / x.time, reverse=True)

        while len(tasks) > 0:
            i = 0
            while not tasks[i].can_be_executed(passed_tasks):
                i += 1
            t = tasks.pop(i)
            passed_tasks[t._id] = True
            schedule.append(t)

        return schedule

    def solve(self, passed_tasks):
        start_time = time.time()

        graph = Graph(directed=True)

        # Add vertexs
        for t in self.tasks:
            graph.add_vertex(t._id)

        # Add dummy vertexs
        graph.add_vertex('DummyStart')
        graph.add_vertex('DummyEnd')

        # Add edges
        for t in self.tasks:
            graph.add_edge('DummyStart', t._id)
            graph.add_edge(t._id, 'DummyEnd')

            for t2 in t.successors:
                graph.add_edge(t2._id, t._id)

        self.graph = graph

        tasks_to_be_scheduled = copy.copy(self.tasks_dict)

        schedule = []
        lamb_min = 0
        while len(tasks_to_be_scheduled) > 0:
            tasks,lamb_min = self.get_next_tasks(tasks_to_be_scheduled, lamb_min)

            if len(tasks) == 1:
                tasks = tasks
            else:
                tasks = SidneyScheduler.greedy_solve(tasks, passed_tasks)

            for t in tasks:
                passed_tasks[t._id] = True
                schedule.append(t)
                del tasks_to_be_scheduled[t._id]

            vertexs = list(tasks_to_be_scheduled.keys())
            vertexs.append('DummyStart')
            vertexs.append('DummyEnd')
            self.graph = self.graph.subgraph(vertexs)

        return schedule,time.time() - start_time
