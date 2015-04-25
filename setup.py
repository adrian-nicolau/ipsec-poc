#!/usr/bin/env python
#
# Script adapted from:
# http://eli.thegreenplace.net/2013/04/20/bootstrapping-virtualenv

import sys
import subprocess


VIRTUALENV_VERSION = '1.9.1'
PYPI_VIRTUALENV_BASE = 'http://pypi.python.org/packages/source/v/virtualenv'
PYTHON = 'python2'
INITIAL_ENV = 'sandbox'
REQUIREMENTS = 'requirements.txt'


def shellcmd(cmd, echo=True):
    """ Run 'cmd' in the shell and return its standard out.
    """
    if echo:
        print '  [cmd]  {0}'.format(cmd)
    ret = subprocess.call(cmd, stderr=sys.stderr, shell=True)
    if echo and ret != 0:
        print '  .....  return code: {0}'.format(ret)
    return ret


def create_virtualenv():
    """ Download archive, extract it and bootstrap a virtual environment.
    """
    dirname = 'virtualenv-' + VIRTUALENV_VERSION
    tgz_file = dirname + '.tar.gz'
    venv_url = PYPI_VIRTUALENV_BASE + '/' + tgz_file

    # Download
    ret = shellcmd('curl -O {0}'.format(venv_url))
    if ret:
        ret = shellcmd('wget -nv {0}'.format(venv_url))
    if ret:
        print 'Give up downloading archive from {0}'.format(venv_url)
        return ret

    # Extract archive
    ret = shellcmd('tar xzf {0}'.format(tgz_file))
    if ret:
        return ret

    # Create the initial environment
    ret = shellcmd('{0} {1}/virtualenv.py {2}'.format(PYTHON, dirname,
                                                      INITIAL_ENV))
    if ret:
        return ret

    # Cleanup
    ret = shellcmd('rm -rf {0} {1}'.format(dirname, tgz_file))
    if ret:
        return ret

    return 0


def setup_environment():
    """ Create a virtual environment and install with pip the requirements.
    """

    ret = create_virtualenv()
    if ret:
        return ret

    ret = shellcmd('{0}/bin/pip install -r {1}'.format(INITIAL_ENV,
                                                       REQUIREMENTS))
    if ret:
        return ret

    return 0


if __name__ == '__main__':
    sys.exit(setup_environment())
