
import datetime
class ViewModel:
    def __init__(self, tasks, show_all_done = False):
        self._tasks = tasks
        self._show_all_done = show_all_done

    @property
    def tasks(self):
        return self._tasks

    @property
    def show_all_done(self):
        return self._show_all_done

    @show_all_done.setter
    def show_all_done(self, value):
        self._show_all_done = value



    def get_to_do_items(self):
        to_dos = [task for task in self.tasks if task.is_to_do()]
        
        return to_dos

    def get_doing_items(self):
        doings = [task for task in self.tasks if task.is_doing()]
        return doings

    def get_done_items(self):
        dones = [task for task in self.tasks if task.is_done()]
        return dones
    
    def is_recently_modified(self, time):
        now = datetime.datetime.now()
        todaymidnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if time < todaymidnight:
            return False
        else:
            return True

        
    def get_recent_done_items(self):
        recent_items = []
        all_done_items = self.get_done_items()
        if (len(all_done_items) < 6 or self.show_all_done):
            print(f"Returning recent items as all done: {all_done_items} show_all_done {self.show_all_done}")
            return all_done_items
        else:
            for item in all_done_items:
                
                modified_time = item.modified_date
                print(f"Modified time for task {item.id} is {modified_time}")
                if(self.is_recently_modified(modified_time)):
                    recent_items.append(item)
        
        print(f"Returning recent items: {recent_items}")
        return recent_items


    def get_older_done_items(self):
        older_items = []
        all_done_items = self.get_done_items()

        for item in all_done_items:
            modified_time = item.modified_date
            print(f"Modified time for task {item.id} is {modified_time}")
            if not self.is_recently_modified(modified_time):
                older_items.append(item)

        print(f"Returning older items as all done: {older_items}")      
        return older_items
