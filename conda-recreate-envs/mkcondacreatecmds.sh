#!/bin/sh

conda_root='/cvmfs/test.galaxyproject.org/deps/_conda'
channel='/cvmfs/test.galaxyproject.org/deps/_conda_tmp/channel'

cd $conda_root/envs

for d in *; do
    for f in $d/conda-meta/*.json; do
        basename $f .json | sed -e 's/\(.*\)-\(.*\)-\(.*\)/\1=\2=\3/'
    done | xargs echo "conda create -c file://$channel --use-local -y -n $d"
done
