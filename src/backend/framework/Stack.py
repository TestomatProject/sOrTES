class Stack:
    def __init__(self):
        self.stack = []

    def put(self, obj):
        self.stack.append(obj)

    def get(self):
        return self.stack.pop()

    def __len__(self):
        return self.stack.__len__()

    def size(self):
        return self.__len__()

    def isEmpty(self):
        return self.size() == 0
