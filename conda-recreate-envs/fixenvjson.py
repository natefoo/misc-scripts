#!/usr/bin/env python

import shutil
import glob
import json
import sys

conda_root = '/cvmfs/test.galaxyproject.org/deps/_conda'
stashfile = 'stash.json'


def get_name_from_meta(meta):
    # could probably also just strip .tar.bz2 from "fn"
    return '{name}-{version}-{build}'.format(
            name=meta['name'],
            version=meta['version'],
            build=meta['build'],
        )


def get_from():
    stash = {}
    for jsonf in glob.glob(conda_root + '/envs/*/conda-meta/*.json'):
        meta = None
        with open(jsonf) as fh:
            meta = json.load(fh)
        name = get_name_from_meta(meta)
        if 'schannel' not in meta:
            if meta['channel'].startswith('https://repo.continuum.io/'):
                meta['schannel'] = 'defaults'
            else:
                meta['schannel'] = meta['channel'].split('/')[3]
        stash[name] = {
                'channel': meta['channel'],
                'schannel': meta['schannel'],
                'url': meta['url'],
                'md5': meta['md5'],
            }
    with open(stashfile, 'w') as fh:
        json.dump(stash, fh, indent=2, separators=(',', ': '), sort_keys=True)


def set_to():
    stash = None
    with open(stashfile) as fh:
        stash = json.load(fh)
    for jsonf in glob.glob(conda_root + '/envs/*/conda-meta/*.json'):
        meta = None
        with open(jsonf) as fh:
            meta = json.load(fh)
        name = get_name_from_meta(meta)
        if meta['url'] != stash[name]['url'] or meta['channel'] != stash[name]['channel']:
            meta['channel'] = stash[name]['channel']
            meta['schannel'] = stash[name]['schannel']
            meta['url'] = stash[name]['url']
            if meta['md5'] != stash[name]['md5']:
                print("WARNING: md5s do not match")
            print("Writing channel '{channel}' url '{url}' to '{json_file}'".format(
                    channel=meta['channel'],
                    url=meta['url'],
                    json_file=jsonf))
        shutil.copy(jsonf, jsonf + '.backup')
        with open(jsonf, 'w') as fh:
            json.dump(meta, fh, indent=2, separators=(',', ': '), sort_keys=True)
            fh.write('\n')


if __name__ == '__main__':
    if sys.argv[1] == 'from':
        get_from()
    elif sys.argv[1] == 'to':
        set_to()
