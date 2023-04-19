from pathlib import Path
from typing import Dict
import sys
from .protocol import Protocol_processor
from subprocess import Popen

path_script = Path(__file__)
sys.path.append(path_script.parent.parent.parent.__str__())

from pkg.logger import new_logger, Timer


class VarNote_processor(Protocol_processor):
    def init_args(self, kwargs: Dict):
        # require
        self.path_varnote = kwargs.get('path_varnote')
        # optional
        self.logger = kwargs.get('logger', new_logger())
        # other
        self.timer = Timer()
        # setUp: input protocol/coordinate to build script
        self.append_setUp(self.set_protocol)
        # run: input vcf/output path to get pid and wait() for process complete
        self.append_run(self.run_io)

    def set_protocol(self, **kwargs):
        "set protocol/annoSrc to build cmd tmpl"
        self.protocol, self.annoSrc = kwargs.get('protocol'), kwargs.get('annoSrc')
        cmd = ['java', '-jar', str(self.path_varnote), 'Annotation']
        cmd += ['-Q:vcf', '{input}', '--maxVariantLength', '10000']
        cmd += ['-D:db,mode=1,tag=%s' % self.protocol, str(self.annoSrc)]
        cmd += ['-O', '{output}', '--is-zip', 'false', '-OF', 'VCF']
        self.cmd = cmd

        return kwargs

    def run_io(self, **kwargs) -> int:
        cmdStr = ' '.join(self.cmd).format(**kwargs)
        pathStrLog = "%s.log" % kwargs['output']
        name_process = '%s-varnote' % self.protocol
        self.timer.start(name_process)
        self.run_process = Popen("%s >%s 2>&1" % (cmdStr, pathStrLog), shell=True)
        code_return = self.run_process.wait()
        if code_return == 0:
            Path(pathStrLog).unlink()
        self.logger.info("%s => %s" % (self.timer.log(name_process), 'complete' if code_return == 0 else 'fail'))
        return code_return
