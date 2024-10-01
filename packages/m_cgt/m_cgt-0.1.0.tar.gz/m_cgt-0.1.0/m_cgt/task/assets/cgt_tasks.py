# -*- coding: utf-8 -*-
import dataclasses
import importlib
import json
import os
from typing import Optional, List, Union

from .. import cgt_task_base

importlib.reload(cgt_task_base)


class CGTTask(cgt_task_base.CGTTaskBase):
    def __init__(self, project_db: str, task_id: str, super_user: bool = False):
        """
            这个类主要是处理当个资产任务的类

        :param project_db: 数据库名字
        :param task_id: 任务id
        """
        super().__init__(project_db, super_user)
        if not task_id:
            raise AttributeError("Invalid task_id")
        self.task_id = task_id

    def get_asset_nm_and_task_nm(self):
        """
            获取资产名和任务名
        :return: AssetTaskName
        :raises AttributeError: 当任务id获取不到资产信息的时候触发的诧异
        """

        @dataclasses.dataclass
        class AssetTaskName:
            asset_name: str
            task_name: str

        data = self.t_tw.task.get(self.project_db, self.module, id_list=[self.task_id],
                                  field_sign_list=["asset.entity", "task.entity"])
        if not data:
            raise AttributeError("task id error")
        for d in data:
            return AssetTaskName(d['asset.entity'], d['task.entity'])

    def get_maya_publish_path(self, pipeline: str):
        """
            获取Maya工程提交路径

        :param pipeline: 流程名
        :return:
        """
        data_path = self.t_tw.task.get_sign_filebox(self.project_db, self.module, self.task_id,
                                                    filebox_sign=f"p_{pipeline.lower()}_maya")["path"]
        name_data = self.get_asset_nm_and_task_nm()
        full_path = os.path.join(data_path, f"{name_data.asset_name}_{name_data.task_name}.ma").replace('\\',
                                                                                                        '/')
        return full_path

    def get_review_path(self, pipeline: str):
        data_path = self.t_tw.task.get_sign_filebox(self.project_db, self.module, self.task_id,
                                                    filebox_sign=f"p_{pipeline.lower()}_review")["path"]
        name_data = self.get_asset_nm_and_task_nm()
        full_path = os.path.join(data_path,
                                 f"{name_data.asset_name}_{name_data.task_name}_v{self.get_next_version()}.png").replace(
            '\\', '/')
        return full_path

    def get_current_version(self) -> str:
        """
            获取当前版本号

        :raises AttributeError: 当任务id获取不到数据时候，触发诧异
        :return: 001 / 002
        """
        fields = self.t_tw.version.fields(self.project_db)
        version_id = self.t_tw.version.get_id(self.project_db, filter_list=[["#link_id", "=", self.task_id]])
        if not version_id:
            return

        version_data = self.t_tw.version.get(self.project_db, id_list=version_id, field_list=fields)
        if not version_data:
            return
        max_version = sorted(version_data, key=lambda x: x["entity"], reverse=True)[0]
        return max_version["entity"]

    def get_next_version(self):
        """
            获取下一个版本号

        :return:
        """
        return str(int(self.get_current_version()) + 1).zfill(3) if self.get_current_version() else "001"

    def get_downstream(self):
        """
            获取下游任务信息
        :return:
        """

        @dataclasses.dataclass
        class DownStreamData:
            asset_name: str
            pipeline: str
            artist_account: str
            artist_name: str
            task_id: str

            def __str__(self):
                return f"{self.asset_name} - {self.pipeline} - {self.artist_account} - {self.artist_name} - {self.task_id}"

            def __hash__(self):
                return hash((self.asset_name, self.pipeline, self.artist_account, self.artist_name, self.task_id))

        down_list = []
        with open(os.path.join(os.path.dirname(__file__), "../../../../config/pipeline.json"), "r",
                  encoding="utf-8") as f:
            pipeline_config = json.load(f)
        current_pipeline_data = pipeline_config["asset"][self.pipeline]
        for downstream in current_pipeline_data:
            downstream_ids = self.get_task_id_with_pipeline(downstream)
            if not downstream_ids:
                continue
            for downstream_id in downstream_ids:
                cgt_downstream = CGTTask(self.project_db, downstream_id)
                artist = cgt_downstream.artist_account
                if not artist:
                    continue
                down_list.append(
                    DownStreamData(self.asset_name, downstream, artist, cgt_downstream.artist_name, downstream_id))
        return tuple(down_list)

    def get_task_id_with_pipeline(self, pipeline: str) -> Optional[Union[str, list]]:
        """
            根据资产名称和流程名获取任务id

        :param pipeline: 流程名
        :return:
        """
        task_id = self.t_tw.task.get_id(self.project_db, self.module,
                                        filter_list=[["asset.entity", "=", self.asset_name], "and",
                                                     ["pipeline.entity", "=", pipeline]])
        if not task_id:
            return
        return task_id

    def get_task_id_with_pipeline_and_task_name(self, pipeline: str, task_name: str) -> Optional[Union[str, list]]:
        """
            根据资产名和流程名和任务名获取任务id

        :param pipeline: 流程名
        :param task_name: 任务名
        :return:
        """
        task_id = self.t_tw.task.get_id(self.project_db, self.module,
                                        filter_list=[["asset.entity", "=", self.asset_name], "and",
                                                     ["pipeline.entity", "=", pipeline], "and",
                                                     ["task.entity", "=", task_name]])
        if not task_id:
            return
        return task_id

    def submit_review(self, review_path: List[str]):
        self.t_tw.task.publish(self.project_db, self.module, self.task_id, path_list=review_path,
                               filebox_sign=f"p_{self.pipeline.lower()}_review", version=self.get_next_version())

    def publish_file(self, files_list: List[str], sign_dir: str, note: Union[str, list] = None) -> bool:
        """
            提交文件

        :param files_list: 提交文件列表
        :param sign_dir: 提交文本框标识符
        :param note: note信息
        :return:
        """
        self.t_tw.task.publish(self.project_db, self.module, self.task_id, files_list, filebox_sign=sign_dir,
                               version=self.get_current_version(), note=note if note else "")
        return True

    def get_version_file(self, sign_dir: str):
        file_list = self.t_tw.task.get_version_file(self.project_db, self.module, [self.task_id], sign_dir)
        return file_list

    def get_task_status(self) -> str:
        """
            获取当前CGT的任务状态

        :return:
        """
        task_data = self.t_tw.task.get(self.project_db, self.module, [self.task_id], field_sign_list=["task.status"])
        if not task_data:
            raise AttributeError("task id error")
        return task_data[0]["task.status"]

    def get_leader_status(self) -> str:
        """
            获取当前CGT的内部审核状态

        :return:
        """
        task_data = self.t_tw.task.get(self.project_db, self.module, [self.task_id],
                                       field_sign_list=["task.leader_status"])
        if not task_data:
            raise AttributeError("task id error")
        return task_data[0]["task.leader_status"]

    def get_sign_dir_path(self, sign_dir: str) -> Optional[str]:
        """
            获取标识目录的路径

        :param sign_dir: 目录标识
        :return:
        """
        data = self.t_tw.task.get_sign_filebox(self.project_db, self.module, self.task_id, filebox_sign=sign_dir)
        if not data:
            raise AttributeError("sign dir error")
        return data["path"]

    def send_message(self, account_id_list: List[str], content: Union[str, list], important: bool) -> bool:
        """
            [{"type":"text","content":"te"},{"type":"a","title":"aa","url":"g:/1.jpg"}, {"type":"image","path":"1.jpg"},\
            {"type":"attachment","path":"1.txt"}]

        :param account_id_list: 通知账号
        :param content: 通知内容
        :param important: 是否是重要消息
        :return:
        """
        return self.t_tw.task.send_msg(self.project_db, self.module, self.task_id, account_id_list, content, important)

    def update_task_status(self, status: str, note: Union[str, list] = ""):
        self.t_tw.task.update_task_status(self.project_db, self.module, [self.task_id], status, note)

    @property
    def module(self) -> str:
        return "asset"

    @property
    def exists(self) -> bool:
        id_list = self.t_tw.task.get_id(self.project_db, self.module, [["task.id", "=", self.task_id]])
        if not id_list:
            return False
        return True

    @property
    def pipeline(self) -> str:
        return self.t_tw.task.get(self.project_db, self.module, [self.task_id], field_sign_list=["pipeline.entity"])[0][
            "pipeline.entity"]

    @property
    def asset_name(self) -> str:
        return self.t_tw.task.get(self.project_db, self.module, [self.task_id], field_sign_list=["asset.entity"])[0][
            "asset.entity"]

    @property
    def task_name(self) -> str:
        return self.t_tw.task.get(self.project_db, self.module, [self.task_id])[0]["task.entity"]

    @property
    def artist_account(self) -> Optional[str]:
        data = self.t_tw.task.get(self.project_db, self.module, [self.task_id], field_sign_list=["task.account"])
        if not data:
            return
        return data[0]["task.account"]

    @property
    def artist_name(self) -> Optional[str]:
        data = self.t_tw.task.get(self.project_db, self.module, [self.task_id], field_sign_list=["task.artist"])
        if not data:
            return
        return data[0]["task.artist"]
