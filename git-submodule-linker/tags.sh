#!/bin/bash

cd slurm-drmaa

for v in {7..0}; do
    for sha in $(git log --format=format:%H); do
        git checkout $sha 2>/dev/null
        #echo -n "$sha "
        ct=$(find . -type d \( -path ./drmaa_utils -o -path ./.git -o -path ./doc \) -prune -o -path ./.ignore -prune -o -type f -exec diff --color -I '$Id' -u ~/slurm-drmaa/tarballs/slurm-drmaa-1.0.${v}/{} {} 2>/dev/null \; | wc -l)
        if [ $ct -lt ${min:-99999} ]; then
            min="$ct"
            min_sha="$sha"
        fi
    done
    git checkout $min_sha 2>/dev/null
    echo "git tag -m 'Tag version 1.0.$v' 1.0.$v $min_sha"
    unset min_sha min
done
