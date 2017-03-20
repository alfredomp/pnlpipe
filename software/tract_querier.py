import os
from software import downloadGithubRepo, getCommitInfo, getSoftDir, checkExists, TemporaryDirectory, envFromDict
from plumbum import local
from plumbum.cmd import cmake, make, chmod
import logging

DEFAULT_HASH = 'e045eab'

def make(commit=DEFAULT_HASH):
    """Downloads a lean version of tract_querier. Output is '$soft/tract_querier-<commit>'."""
    dest = getSoftDir()

    if commit != 'master':
        out = local.path(dest / 'tract_querier-' + commit)
        if checkExists(out):
            return

    with TemporaryDirectory() as tmpdir, local.cwd(tmpdir):
        repo = downloadGithubRepo('demianw/tract_querier', commit)
        sha, date = getCommitInfo(repo)
        out = local.path(dest / 'tract_querier-' + sha)
        if checkExists(out):
            return

        # save space
        (repo / 'doc').delete()
        (repo / '.git').delete()

        logging.info("Make '{out}'".format(**locals()))
        repo.move(out)

    chmod('-R', 'a-w', out)
    chmod('a-w', out)
    date_symlink = dest / 'tract_querier-' + date
    out.symlink(date_symlink)


def getPath(hash=DEFAULT_HASH):
    path = getSoftDir() / ('tract_querier-' + hash)
    if not path.exists():
        raise Exception(
            "{} doesn\'t exist, make it first with 'pnlscripts/software.py --commit {} tractquerier".format(
                path, hash))
    return path

def envDict(hash):
    return {'PATH': getPath(hash) / 'scripts'
           ,'PYTHONPATH': getPath(hash)
    }

def env(bthash):
    return envFromDict(envDict(bthash))
