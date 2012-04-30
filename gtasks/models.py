# -*- coding: utf-8 -*-
"""
    gtasks.models
    ~~~~~~~~~~~~~


    :copyright: (c) 2012 by Daisuke Igarashi.
    :license: BSD, see LICENSE for more details.
"""


class Link(object):
    type = "" # e.g. "email"
    description = ""
    link = ""
    def __str__(self):
        return {"type":self.type, "description":self.description, "link":self.link}

#{u'status': u'needsAction', u'kind': u'tasks#task', u'title': u'http://culture.rouxril.com/2011/08/post-108.php', u'updated': u'2011-08-30T06:15:15.000Z', u'etag': u'"tYmMMv-zuHYx-tb4P1tsenocCRI/LTEzMzM0NjAxODU"', u'position': u'00000000000000000123', u'id': u'MDY4MDA3NzIzMDExMjk4NDg1MTY6MDoxOTkwMDcwMzA1', u'selfLink': u'https://www.googleapis.com/tasks/v1/lists/MDY4MDA3NzIzMDExMjk4NDg1MTY6MDow/tasks/MDY4MDA3NzIzMDExMjk4NDg1MTY6MDoxOTkwMDcwMzA1'}
class Task(object):
    kind = "tasks#task"
    id = ""
    etag = ""
    title = ""
    updated = "" #datetime
    selfLink = ""
    parent = ""
    position = 0
    notes = ""
    status = "" #needsAction, completed
    due = "" #datetime
    completed = "" #datetime
    deleted = False
    hidden = False #readonly
    links = [] # list of Link

    def __init__(self, task={}):
        self.__dict__.update(task)
    
#{u'kind': u'tasks#taskList', u'updated': u'2011-09-03T13:30:29.000Z', u'id': u'MDY4MDA3NzIzMDExMjk4NDg1MTY6MDow', u'selfLink': u'https://www.googleapis.com/tasks/v1/users/@me/lists/MDY4MDA3NzIzMDExMjk4NDg1MTY6MDow', u'title': u'planset\u3055\u3093\u306e\u30ea\u30b9\u30c8'}
class TaskList(object):
    id = ""
    title = ""
    kind = "tasks#task"
    updated = ""
    
    def __init__(self, tasklist={}):
        self.__dict__.update(tasklist)
    

