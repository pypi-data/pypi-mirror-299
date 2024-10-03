#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tasks.py
@Time    :   2024-08-16 13:50:45
@Author  :   chakcy 
@Email   :   947105045@qq.com
@description   :   tasks
'''

from ..model import Request
from ..constants import TaskStatus


class Tasks():
    TaskClasses = {}

    @classmethod
    def append_Task(cls, task_name:str, task_class:object):
        cls.TaskClasses[task_name] = task_class

    @classmethod
    def run_task(cls, request:Request):
        task_name = request.task_name
        TaskClass = cls.TaskClasses.get(task_name, None)
        if TaskClass == None:
            return {
                "task_name": task_name,
                "id": "null",
                "error": "Task not found",
                "status": TaskStatus.FAILED,
                "created_at": "null",
                "updated_at": "null"
            }
        result = TaskClass(id=request.id, params=request.args).result_callback() if request.args is not None else TaskClass().result_callback() # type: ignore
        return result
    