#!/bin/sh
set -e

user=g2test
conda_root='/cvmfs/test.galaxyproject.org/deps/_conda'

cd $conda_root/envs

for d in *; do
    echo "[$d]"
    for f in $d/conda-meta/*.json; do
        cmd="rsync -avP $conda_root/pkgs/$(basename $f .json) $user@galaxy04:$conda_root/pkgs"
        echo "$cmd"
        $cmd
    done
done
