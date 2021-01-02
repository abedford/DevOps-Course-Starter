
import datetime
class ViewModel:
    def __init__(self, tasks):
        self._tasks = tasks
        self._show_all_done = False

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

    def show_all_done_items(self):
        return self._show_all_done
    
    def is_recently_modified(self, time):
        now = datetime.datetime.now()
        todaymidnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if time < todaymidnight:
            print(f"{time} is before today midnight {todaymidnight} so marking as not recently modified")
            return False
        else:
            print(f"{time} is not before today midnight {todaymidnight} so marking as recently modified")
            return True

        
    def get_recent_done_items(self):
        recent_items = []
        all_done_items = self.get_done_items()
        if (len(all_done_items) < 6):
            return all_done_items
        else:
            for item in all_done_items:
                # get a modified date for this item
                # check if it's todays
                modified_time = item.modified_date
                print(f"Modified time for task {item.id} is {modified_time}")
                if(self.is_recently_modified(modified_time)):
                    recent_items.append(item)
                
        return recent_items

    def get_older_done_items(self):
        return None


#     show_all_done_items: which will keep track of if we
#       should show all the completed items, or just the most
#       recent ones.
# • 
#       recent_done_items: which will return all the tasks that
#       have been completed today.
# •         older_done_items: which will return all of the tasks that
#       were completed before today.