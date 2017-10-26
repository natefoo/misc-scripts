Miscellaneous Scripts
=====================

I've written many scripts over the years. Most of them end up in the bit
bucket, but I decided that a few that might occasionally be useful to other
people or that I might want to refer back to some day ought to be preserved.
And here we are.

Contents
--------

### conda-recreate-envs

[conda-recreate-envs](tree/master/conda-recreate-envs)

I needed to upgrade from miniconda2 3.19 to miniconda3 4.3 and, in the process,
recreate all of the existing envs with all packages and dependencies at the
exact versions of when they were created. Unfortunately, Continuum had removed
some of the necessary packages from their channel, and I had removed some of
the tarballs in `pkgs`, meaning that they had to be refetched (when possible)
and recreated from the unpacked package (when not).

### prunesnaps

Prune ZFS snapshots on a rolling basis, keeping snapshots at larger time
intervals as they get older.
