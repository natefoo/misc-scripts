#!/bin/bash
set -e

conda_root='/cvmfs/test.galaxyproject.org/deps/_conda'
tbdir=$(pwd)/tarballs

[ ! -d $tbdir ] && mkdir -p $tbdir

cd $conda_root/pkgs

for d in $(find -maxdepth 1 ! -path . -type d -printf '%P\n'); do
    tb="$d.tar.bz2"
    savetb="$tbdir/$tb"
    if [ -f $tb -a ! -f $savetb ]; then
        echo "saving existing $tb"
        cp $tb $savetb
    elif [ ! -f $tb -a ! -f $savetb ]; then
        continue_me=0
        for json in $conda_root/envs/*/conda-meta/$d.json; do
            if [ "$json" == "$conda_root/envs/*/conda-meta/$d.json" ]; then
                # if the package is not part of an env we probably don't care about it anyway
                echo "warning: no env json found for $d, skipping"
                continue_me=1
                break
            fi
            read pkgurl pkgmd5 < <(python -c "import json; x = json.load(open('$json')); print x['url'], x['md5']")
            [ -n "$pkgurl" ] && break
        done
        [ $continue_me -eq 1 ] && continue
        if [ -n "$pkgurl" ]; then
            echo "fetching $pkgurl obtained from $json"
            curl -L $pkgurl >$savetb
            [ $(md5sum -b $savetb | awk '{print $1}') == "$pkgmd5" ] || rm $savetb
        fi
        if [ ! -f $savetb ]; then
            echo "creating $d.tar.bz2 from unpacked pkg"
            cd $d
            tar jcf $savetb $(find -maxdepth 1 ! -path . -type d -printf '%P ')
            cd ..
        fi
    fi
done
