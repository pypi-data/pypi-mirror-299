import unittest
from ..cgt_tasks import CGTTask


class MyTestCase(unittest.TestCase):
    def test_something(self):
        cgt_task = CGTTask(project_db="proj_temp_test",task_id="06341EC4-94FC-3EB6-38E9-0ACD58F45AEA")
        print(cgt_task.get_current_version())
