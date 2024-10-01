# -*- coding: utf-8 -*-
import importlib
from .. import cgt_base
from ..info.cgt_account import *

importlib.reload(cgt_base)


class CGTTaskBase(cgt_base.MyCGTeamWork):
    def __init__(self, project_db: str, super_user: bool = False):
        super().__init__(super_user)
        self.project_db = project_db
