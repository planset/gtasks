# -*- coding: utf-8 -*-
"""
    gtasks.google_tasks_ui
    ~~~~~~~~~~~~~~~~~~~~~~


    :copyright: (c) 2012 by Daisuke Igarashi.
    :license: BSD, see LICENSE for more details.
"""

from gtasks.models import Task
from gtasks.models import TaskList
from gtasks.tools import clear_screen


DEFAULT_TASKLIST = '@default'

class GoogleTasksUI(object):
    service = None
    tasklists = None
    tasks = None
    current_tasklist = DEFAULT_TASKLIST
    current_page = 1
    num_of_page = 10
    
    def _print(self, msg):
        if self.scr:
            msg = " " + msg + "\n"
            self.scr.addstr(msg)
        else:
            print msg
            
    def __init__(self, service, scr=None, num_of_page=10):
        self.service = service
        self.scr = scr
        self.num_of_page = num_of_page
        self.update_tasklists()
        self.update_tasks()
        # api actions
        self.actions = {
                "p":self.move_prev,
                "n":self.move_next,
                "a":self.add_task,
                "d":self.delete_task, 
                "r":self.rename_task, 
                "c":self.complete_task, 
                "l":self.clear_completed_tasks, 
                "m":self.move_task, 
                "s":self.show_tasks,
                "t":self.change_tasklists}
    
    def _get_tasklists(self):
        self.tasklists = [TaskList(i) for i in self.service.tasklists().list().execute()["items"]]
        
    def _get_tasks(self, tasklist_name):
        self.tasks = [Task(i) for i in self.service.tasks().list(tasklist=tasklist_name).execute()["items"]]

    def _print_tasks(self, page, num_of_page):
        index_start = (page - 1) * num_of_page
        index_end = index_start + num_of_page
        if index_end > len(self.tasks):
            index_end = len(self.tasks) 
        for i in range(index_start, index_end):
            self._print_task(i+1, self.tasks[i])
        
    def _print_task(self, index, task):
        comp = " "
        if task.completed:
            comp = 'x'
        self._print(u"{index:>2} {comp} {title}".format(index=index, comp=comp, title=task.title))

    def _get_current_page_index(self, index):
        """表示しているタスクの番号からself.tasksのインデックスを取得"""
        return (self.current_page - 1) * self.num_of_page + index - 1
        
    def show_help(self, opt=""):
        if opt:
            if opt == "a":
                self._print("Add: a TITLE [NOTE]")
        else:
            self._print("p:Prev   n:Next ")
            self._print("a:Add    c:Complete")
            self._print("r:Rename d:Delete")
            self._print("s:Show   m:Move ")
            self._print("l:Clear completed tasks")
            self._print("t:Change tasklists ")
            self._print("q:Quit")
        
    def move_next(self):
        'Move next page'
        if (self.current_page+1-1)*self.num_of_page < len(self.tasks):
            self.current_page += 1
        self._print_tasks(self.current_page, self.num_of_page)
            
    def move_prev(self):
        'Move prev page'
        if self.current_page-1 >= 1:
            self.current_page -= 1
        self._print_tasks(self.current_page, self.num_of_page)
            
    def show_tasks(self):
        'Show tasks'
        clear_screen()
        self._print_tasks(self.current_page, self.num_of_page)

    def change_tasklists(self):
        'Show tasklist'
        for index,tasklist in enumerate(self.tasklists):
            self._print(u"{index:>2} : {title}".format(
                    index=index,
                    title=tasklist.title))
        tasklist_index = int(raw_input('Tasklist id: '))
        if 0 <= tasklist_index and tasklist_index < len(self.tasklists):
            self.current_tasklist = self.tasklists[tasklist_index].id
            self.update_tasks()

    def update_tasklists(self):
        'Update tasklists'
        self._get_tasklists()

    def update_tasks(self):
        'Update tasks'
        self._get_tasks(self.current_tasklist)

    def add_task(self):
        'Add task'
        name = raw_input('Task name: ')
        body = {"title": name}
        self.service.tasks().insert(tasklist=self.current_tasklist, body=body).execute()
        self.update_tasks()
    
    def delete_task(self):
        'Delete task'
        index = int(raw_input('Task index: '))
        index = self._get_current_page_index(index)
        task = self.tasks[index]
        self.service.tasks().delete(tasklist=self.current_tasklist, task=task.id).execute()
        del(self.tasks[index])

    def rename_task(self):
        'Rename task'
        index = int(raw_input('Task index: '))
        new_name = raw_input('Task new name: ')
        index = self._get_current_page_index(index)
        task = self.tasks[index]
        task.title = new_name
        self.service.tasks().update(tasklist=self.current_tasklist, task=task.id, body=task.__dict__).execute()

    def complete_task(self):
        'Complete task'
        index = int(raw_input('Task index: '))
        index = self._get_current_page_index(index)
        task = self.tasks[index]
        task.status = "completed"
        self.service.tasks().update(tasklist=self.current_tasklist, task=task.id, body=task.__dict__).execute()

    def clear_completed_tasks(self):
        'Clear completed tasks'
        self.service.tasks().clear(tasklist=self.current_tasklist).execute()

    def move_task(self):
        'Move task up or down'
        index = int(raw_input('Task index: '))
        pos = int(raw_input('Move to: '))
        index = self._get_current_page_index(index)
        task = self.tasks[index]
        task.pos = pos
        self.service.tasks().move(tasklist=self.current_tasklist, task=task.id, body=task.__dict__ ).execute()


