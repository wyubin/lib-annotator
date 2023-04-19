from typing import Dict
from pathlib import Path
import yaml

from .pkg.logger import new_logger
from .pkg.info import Protocol_info
from .pkg.processor import Protocol_processor, VarNote_processor

pathDir = Path(__file__).parent


class Annotator():
    def __init__(self, conf: Dict[str, str], logger=None):
        self.args = {}
        self.logger = logger or new_logger()
        self.setUp(**conf)
        self.loadDBVersion()
    
    def setUp(self, **conf):
        _default = {'varNote': str(pathDir.joinpath('bin', 'VarNote.jar'))}
        for x in ['hg19', 'hg38', 'varNote']:
            self.args[x] = conf.get(x, _default.get(x))

    def loadDBVersion(self):
        _conf = yaml.load(pathDir.joinpath('conf', 'versionControl.yaml').open(), Loader=yaml.FullLoader)
        self.versionControl = Protocol_info(_conf, self.logger)
        self.versionControl.setUp(**self.args)

    def get_processor(self, protocol: str, coordinate: str) -> Protocol_processor:
        processor = VarNote_processor(path_varnote=self.args['varNote'], logger=self.logger)
        annoSrc = self.versionControl.get_protocol_path(protocol, coordinate)
        processor.setUp(protocol=protocol, annoSrc=annoSrc)

        return processor
