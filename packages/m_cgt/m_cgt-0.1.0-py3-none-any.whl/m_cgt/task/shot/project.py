# -*- coding: utf-8 -*-
import dataclasses
from typing import List

from ..cgt_task_base import CGTTaskBase
from ...errors.cgteamwork_error import HasAnyShotTask
from ...info.cgt_account import CGTAccount


@dataclasses.dataclass
class ShotData:
    id: str
    eps_number: str
    seq_number: str
    shot_number: str
    status: str
    fps: str

    def __hash__(self):
        return hash((self.eps_number, self.shot_number, self.seq_number, self.status, self.fps))


class CGTShotTaskProject(CGTTaskBase):
    def __init__(self, project_db: str, super_user: bool = False):
        super().__init__(project_db, super_user)
        self.cgt_account = CGTAccount()

    def get_my_task_with_pipeline(self, pipeline: str) -> List[ShotData]:
        """
            用流程名获取我的任务

        :param pipeline: 流程名
        :return:
        :raises HasAnyShotTask: 当程序获取不到任何镜头数据时候触发
        """
        current_user = self.cgt_account.current_user
        task_id_list = self.t_tw.task.get_id(self.project_db, self.module,
                                             filter_list=[["pipeline.entity", "=", pipeline], "and",
                                                          ["task.account","has", current_user]])
        if not task_id_list:
            raise HasAnyShotTask(self.project_db)
        task_data = self.t_tw.task.get(self.project_db, self.module, id_list=task_id_list, field_sign_list=self.fields)
        return [ShotData(id=i["task.id"],
                         eps_number=i["eps.entity"],
                         seq_number=i["shot.link_seq"],
                         shot_number=i["shot.entity"],
                         status=i["task.status"],
                         fps=i["shot.frame"]) for i in task_data]

    @property
    def module(self):
        return "shot"

    @property
    def fields(self):
        return self.t_tw.task.fields(self.project_db, self.module)
