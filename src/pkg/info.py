from typing import Dict
from .logger import new_logger
from pathlib import Path


class Protocol_info:
    "manage protocol info"

    def __init__(self, info: Dict[str, Dict], logger=None):
        self.info = info
        self.logger = logger or new_logger()

    def setUp(self, **conf):
        self.coordinate2dir = {x: conf.get(x) for x in ['hg19', 'hg38']}
    
    def get_protocol_path(self, protocol: str, coordinate: str) -> Path:
        pathStrCoor = self.coordinate2dir.get(coordinate)
        if pathStrCoor is None:
            self.logger.error("coordinate[%s] not exist" % coordinate)
            return None
        filename = self.get_protocol_filename(protocol, coordinate)
        if filename is None:
            return None
        pathDB = Path(pathStrCoor).joinpath(filename)
        if not pathDB.exists():
            self.logger.error("file[%s] not exist" % pathDB)
            return None
        return pathDB

    def get_protocol_filename(self, protocol: str, coordinate: str) -> str:
        info_protocol = self.info.get(protocol)
        if info_protocol is None:
            self.logger.error("protocol[%s] not exist" % protocol)
            return None
        filename = info_protocol.get('annotatorInfo', {}).get('dataFileName', {}).get(coordinate)
        if filename is None:
            self.logger.error("coordinate[%s] no set db for protocol[%s]" % (coordinate, protocol))
        return filename
