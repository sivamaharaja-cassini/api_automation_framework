# utils/data_manager.py
from typing import List

class DataManager:
    def __init__(self):
        self._created = []  # list of tuples (client, delete_fn, id)

    def track(self, delete_callable, identifier):
        """
        delete_callable: a callable that will delete resource when called with identifier
        identifier: resource id
        """
        self._created.append((delete_callable, identifier))

    def cleanup(self):
        errors = []
        for delete_callable, identifier in reversed(self._created):
            try:
                delete_callable(identifier)
            except Exception as e:
                errors.append(str(e))
        self._created.clear()
        return errors