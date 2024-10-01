# -*- coding: utf-8 -*-
import dataclasses
from typing import Tuple, List

from ..cgt_task_base import CGTTaskBase
from ...modules.version_data import VersionData


@dataclasses.dataclass
class AccountData:
    id: str
    name: str
    account: str

    def __hash__(self):
        return hash(self.id)


class CGTShotTask(CGTTaskBase):
    def __init__(self, project_db: str, task_id: str, super_user: bool = False):
        super().__init__(project_db, super_user)
        self.task_id = task_id

    def get_sign_dir_path(self, sign: str) -> str:
        """
            根据filebox标识符获取路径
        :param sign: 标识符
        :raises AttributeError: 没有这个标识符时候，触发
        :return:
        """
        file_box_data = self.t_tw.task.get_sign_filebox(self.project_db, self.module, self.task_id, sign)
        if not file_box_data:
            raise AttributeError(f"sign: {sign} not found")
        return file_box_data["path"]

    def get_versions(self) -> Tuple[VersionData, ...]:
        """
            获取当前task id任务全部版本信息

        :raises AttributeError: 当没有版本信息时候触发诧异
        :return:
        """
        version_id_list = self.t_tw.version.get_id(self.project_db, [["#link_id", "=", self.task_id]])
        if not version_id_list:
            raise AttributeError(f"version_id not found: {self.task_id}")
        version_data = self.t_tw.version.get(self.project_db, version_id_list,
                                             field_list=self.t_tw.version.fields(self.project_db))
        version_data = [
            VersionData(create_by=i["create_by"], create_time=i["create_time"], description=i["description"],
                        entity=i["entity"], last_update_by=i["last_update_by"], last_update_time=i["last_update_time"],
                        link_entity=i["link_entity"]) for i in version_data]
        return tuple(version_data)

    def get_max_version(self) -> VersionData:
        """
            获取最大版本

        :raises AttributeError: 当没有版本信息时候触发诧异
        :return:
        """
        version_data = self.get_versions()
        return sorted([i for i in version_data], key=lambda x: x.entity)[-1]

    def get_task_id_with_pipeline(self, eps: str, seq: str, shot_number: str, pipeline: str) -> list:
        """
            获取其他流程的id
        :param eps: 集数
        :param seq: 场次
        :param shot_number: 镜头号
        :param pipeline: 流程名
        :raises AttributeError： 当获取不到时候触发诧异
        :return:
        """
        task_id = self.t_tw.task.get_id(self.project_db, self.module,
                                        filter_list=[["eps.entity", "=", eps], "and",
                                                     ["shot.link_seq", "=", seq], "and",
                                                     ["shot.entity", "=", shot_number], "and",
                                                     ["pipeline.entity", "=", pipeline]])
        if not task_id:
            raise AttributeError(f"task_id not found: {pipeline}")
        return task_id

    def get_artist_data(self) -> Tuple[AccountData, ...]:
        """
            获取任务制作者信息

        :raises AttributeError: 当获取不到制作者时候触发
        :return:
        """
        data = self.t_tw.task.get(self.project_db, self.module, [self.task_id],
                                  ["task.artist", "task.account", "task.account_id"])
        if not data:
            raise AttributeError(f"account data not found: {self.task_id}")
        return tuple(
            [AccountData(id=i["task.account_id"], name=i["task.artist"], account=i["task.account"]) for i in data])

    def send_message(self, account_id_list: List, content: str, important: bool = False) -> bool:
        """
            发送信息

        :param account_id_list: @列表 传入id
        :param content: 发送内容
        :param important: 是否是重要信息
        :return:
        """

        return self.t_tw.task.send_msg(self.project_db, self.module, self.task_id, account_id_list, content, important)

    @property
    def module(self):
        return "shot"
