conda-recreate-envs
===================

How to use:

oldhost = host w/ good conda pkgs/envs
newhost = host w/ new conda you are trying to recreate from old

In my case I was working from a CVMFS-installed conda, so the path was the same
on oldhost and newhost (newhost was just working inside an open transaction).
In a more traditional case you might have two conda installs at different paths
on the same host.

1. on oldhost:

    a. run `repkg.sh` to copy/fetch/create tarballs
    b. `rsync -avP tarballs/* newhost:/path/to/index/noarch`
    c. run `fixenvjson.py from` to create stash.json
    d. run `mkcondacreatecmds.sh >createcmds.sh`
    e. `scp stash.json createcmds.sh newhost:/path/to/work`

2. on newhost:

    a. `conda index /path/to/index/noarch`
    b. run createcmds.sh to create envs
    c. run `fixenvjson.py to` to fix up env pkg jsons
    d. `rm envs/*/conda-meta/*.backup pkgs/urls.txt.backup` once satisfied
