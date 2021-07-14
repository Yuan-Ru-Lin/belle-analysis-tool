import pathlib
import urllib
import argparse
import glob


class TreatDataAsMCError(ValueError):
    pass


class SubmitError(ValueError):
    pass


class SubmitInfo:

    def __init__(self, args=None):
        self.kwargs = vars(args)
        self._isMC = self.kwargs['job_kind'] != 'data'
        self._url = _get_belle_url(self.kwargs) if self.kwargs['job_kind'] in ['data', 'mc'] else glob.glob(self.kwargs['path'] + '/*.mdst')
        self._outputname = _get_output_name(**self.kwargs)

        pathlib.Path(self.kwargs['outputDir']).mkdir(parents=True, exist_ok=True)

    @property
    def isMC(self):
        return self._isMC

    @property
    def url(self):
        return self._url

    @property
    def outputname(self):
        return self._outputname

    @property
    def generic(self):
        if self.kwargs['job_kind'] == 'file':
            return False
        elif self.kwargs['job_kind'] == 'mc':
            return True
        else:
            raise TreatDataAsMCError('You are treating Data as MC!')


def build_parser():
    parser = argparse.ArgumentParser()
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('--outputDir', default='.')

    subparsers = parser.add_subparsers(help='Types of data', dest='job_kind')
    data_parser = subparsers.add_parser('data', parents=[common])
    mc_parser = subparsers.add_parser('mc', parents=[common])
    file_parser = subparsers.add_parser('file', parents=[common])

    data_parser.add_argument('ex')
    data_parser.add_argument('rs')
    data_parser.add_argument('re')
    data_parser.add_argument('skm', choices=['HadronB', 'HadronBJ'])
    data_parser.add_argument('dt', default='on_resonance', choices=['on_resonance', 'continuum'])
    data_parser.add_argument('bl', default='caseB')
    data_parser.set_defaults(get_url=_get_belle_url_data)

    mc_parser.add_argument('ex', default='55')
    mc_parser.add_argument('rs', default='990')
    mc_parser.add_argument('re', default='1093')
    mc_parser.add_argument('ty', default='evtgen-uds', choices=['evtgen-uds', 'evtgen-charm', 'evtgen-mixed', 'evtgen-charged'])
    mc_parser.add_argument('dt', default='on_resonance', choices=['on_resonance', 'continuum'])
    mc_parser.add_argument('bl', default='caseB')
    mc_parser.add_argument('st', default='0')
    mc_parser.set_defaults(get_url=_get_belle_url_mc)

    file_parser.add_argument('path')
    file_parser.add_argument('suffix')

    return parser


def _get_belle_url_mc(params):
    return 'http://bweb3/montecarlo.php?' + urllib.parse.urlencode(params)


def _get_belle_url_data(params):
    return 'http://bweb3/mdst.php?' + urllib.parse.urlencode(params)


def _get_file_basename(**kwargs):
    info = kwargs['path'].split('/')
    streamNo, expNo = info[-2:]
    return '_'.join([streamNo, expNo, kwargs['suffix']]) + '.root'


def _get_belle_url(**kwargs):
    if kwargs['job_kind'] == 'mc':
        return _get_belle_url_mc(**kwargs)
    elif kwargs['job_kind'] == 'data':
        return _get_belle_url_data(**kwargs)
    else:
        raise SubmitError(f'Something wrong in your submit info: {kwargs}')


def _get_output_name(**kwargs):
    outputDir = kwargs['outputDir'] + '/'
    if kwargs['job_kind'] == 'file':
        basename = _get_file_basename(**kwargs)
    elif kwargs['job_kind'] == 'mc':
        basename = '_'.join(kwargs[key]
            for key in ['job_kind', 'ex', 'rs', 're', 'ty', 'dt', 'bl', 'st']) + '.root'
    else:
        basename = '_'.join(kwargs[key]
            for key in ['job_kind', 'ex', 'rs', 're', 'skm', 'dt', 'bl']) + '.root'
    return outputDir + basename

