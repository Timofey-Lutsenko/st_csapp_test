
class Queue:
    def __init__(self):
        self.queue = []

    def push(self, item):
        self.queue.append(item)

    def pop(self):
        if len(self.queue) == 0:
            return None
        removed = self.queue.pop(0)
        return removed


class Task:
    def __init__(self, task_str, task_id, status):
        self.task = task_str
        self.task_id = task_id
        self.status = status

    def task_status_updater(self):
        if self.status == 'In queue.':
            self.status = 'In progress.'
        if self.status == 'In progress.':
            self.status = 'Done.'
        else:
            self.status = 'Status Unknown'
        status = self.status
        return status