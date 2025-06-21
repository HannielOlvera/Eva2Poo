from typing import Any, Dict, List
from app.api_client import APIClient
from app.controllers.base_controller import BaseController
from app.controllers.actions import TaskAction
from app.models.simple_task import SimpleTask

class TaskController(BaseController):
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    def get_entities(self) -> List[SimpleTask]:
        raw = self._handle_request(self.api_client.get_tasks)
        tasks: List[SimpleTask] = []
        for t in raw:
            uid = t.get('user_id')
            if isinstance(uid, str) and uid.isdigit():
                t['user_id'] = int(uid)
            try:
                tasks.append(SimpleTask(**t))
            except Exception as e:
                print(f"[WARNING] parsing task {t.get('id')}: {e}")
        return tasks

    def perform_action(self, action: TaskAction, **kwargs: Any) -> Any:
        mapping = {
            TaskAction.ADD:      lambda **kw: self.api_client.add_task(
                                        kw['user_id'], kw['text'], kw['last_modified_by']),
            TaskAction.EDIT:     lambda **kw: self.api_client.edit_task(
                                        kw['task_id'], kw['text'], kw['last_modified_by']),
            TaskAction.DELETE:   lambda **kw: self.api_client.delete_task(kw['task_id']),
            TaskAction.COMPLETE: lambda **kw: self.api_client.complete_task(
                                        kw['task_id'], kw['last_modified_by']),
        }
        func = mapping.get(action)
        if not func:
            raise ValueError(f"Unknown action: {action}")
        return self._handle_request(func, **kwargs)