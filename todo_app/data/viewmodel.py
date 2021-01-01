class ViewModel:
    def __init__(self, tasks):
        self._tasks = tasks

    @property
    def tasks(self):
        return self._tasks

    def get_to_do_items(self):
        to_dos = [task for task in self.tasks if task.is_to_do()]
        
        return to_dos

    def get_doing_items(self):
        doings = [task for task in self.tasks if task.is_doing()]
        return doings

    def get_done_items(self):
        dones = [task for task in self.tasks if task.is_done()]
        return dones