import pathlib
import urllib
import argparse


class SubmitInfo:

    def __init__(self, args=None):
        self.parser = _build_parser()
        self.args = self.parser.parse_args() if args is None else self.parser.parse_args(args.split())

        self.output_directory_path = pathlib.Path(self.args.outputDir)
        self.output_directory_path.mkdir(parents=True, exist_ok=True)

        self._startsWithHttp = len(self.args.path) == 1 and self.args.path[0].startswith('http://')
        self._parse_result = urllib.parse.urlparse(self.url) if self._startsWithHttp else None

    @property
    def isCustomFile(self):
        return not self._startsWithHttp

    @property
    def url(self):
        return self.args.path if self.isCustomFile else self.args.path[0]

    @property
    def isMC(self):
        return self.isCustomFile or self._parse_result.path == '/montecarlo.php'

    @property
    def outputname(self):
        directory = self.output_directory_path.absolute().as_posix()
        labels = (self.args.path[0].split('/')[-3:-1] + [self.args.suffix] if self.isCustomFile
                else [value[0] for value in urllib.parse.parse_qs(self._parse_result.query).values()])
        basename = '_'.join(labels)
        return f'{directory}/{basename}.root'


def _build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default=['http://bweb3/montecarlo.php?ex=55&rs=990&re=1093&ty=evtgen-uds&dt=on_resonance&bl=caseB&st=0'], nargs='+')
    parser.add_argument('--suffix', default='')
    parser.add_argument('--outputDir', default='.')
    return parser

