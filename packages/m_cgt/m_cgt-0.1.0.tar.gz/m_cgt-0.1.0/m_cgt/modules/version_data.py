# -*- coding: utf-8 -*-
import dataclasses


@dataclasses.dataclass
class VersionData:
    create_by: str
    create_time: str
    description: str
    entity: str
    last_update_by: str
    last_update_time: str
    link_entity: str

    def __hash__(self):
        return hash((self.create_by, self.create_time, self.description, self.entity))
