#!/usr/bin/env python

import os.path
import hashlib
import shutil
import glob
import json
import sys

conda_root = '/cvmfs/main.galaxyproject.org/deps/_conda'
channel = '/home/g2main/conda/noarch'
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
        print jsonf
        with open(jsonf) as fh:
            meta = json.load(fh)
        name = get_name_from_meta(meta)
        if 'schannel' not in meta and 'channel' not in meta:
            if meta['url'].startswith('https://repo.continuum.io/'):
                meta['channel'] = 'https://repo.continuum.io/pkgs/free/linux-64/'
            else:
                meta['channel'] = os.path.dirname(meta['url']) + '/'
        if 'schannel' not in meta:
            if meta['channel'].startswith('https://repo.continuum.io/'):
                meta['schannel'] = 'defaults'
            else:
                meta['schannel'] = meta['channel'].split('/')[3]
        if 'md5' not in meta:
            md5 = hashlib.md5()
            md5.update(open('tarballs/%s' % os.path.basename(meta['url']), 'rb').read())
            meta['md5'] = md5.hexdigest()
        print meta['schannel'], meta['channel'], meta['url']
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
    # fix env pkg json files
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
    # fix urls.txt
    urls = []
    urlsf = conda_root + '/pkgs/urls.txt'
    with open(urlsf) as fh:
        for url in fh:
            if url.startswith('file://' + channel):
                name = url.split('/')[-1].replace('.tar.bz2\n', '')
                if name in stash:
                    url = stash[name]['url'] + '\n'
                else:
                    print("Can't fix urls.txt entry for '{name}': not in stash".format(name=name))
            urls.append(url)
    shutil.copy(urlsf, urlsf + '.backup')
    with open(urlsf, 'w') as fh:
        fh.write(''.join(urls))


if __name__ == '__main__':
    if sys.argv[1] == 'from':
        get_from()
    elif sys.argv[1] == 'to':
        set_to()
