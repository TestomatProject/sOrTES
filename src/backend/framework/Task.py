class Task:
    def __init__(self, _id, time, score, dependencies = None, successors = None):
        self._id = _id
        self.time = float(time)
        self.score = float(score)
        if dependencies is None:
            self.dependencies = []
        else:
            self.dependencies = dependencies

        if successors is None:
            self.successors = []
        else:
            self.successors = successors

    def add_dependency(self, task):
        if task not in self.dependencies:
            self.dependencies.append(task)

    def add_successor(self, task):
        if task not in self.successors:
            self.successors.append(task)

    def can_be_executed(self, passed_tasks):
        return Task.all_tasks_in_dict(self.dependencies, passed_tasks)

    def all_successors_in_dict(self, tasks_dict):
        return Task.all_tasks_in_dict(self.successors, tasks_dict)

    def all_dependencies_not_in_dict(self, tasks_dict):
        for t in self.dependencies:
            if t in tasks_dict:
                return False
        return True

    def all_tasks_in_dict(tasks, task_dict):
        for t in tasks:
            if t._id not in task_dict:
                return False
        return True
