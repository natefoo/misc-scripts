#!/usr/bin/env python3
#
# For SVN->Git conversions w/ SVN externals. Assumes a linear history (because SVN).
#
# SVN does not store the external revision in parent repo revisions, it just gets the latest. So we assume the newest commit on the external at the time of the parent commit is the correct commit
#
# This ended up quite a mess. I'm not going to put any effort into improving this since it got the job done.
#

import argparse
import os
import shlex
from subprocess import CalledProcessError, check_call, check_output

from colorama import Fore


debug = True


def green(*args, **kwargs):
    print(Fore.GREEN, *args, Fore.RESET, **kwargs)


def _parse_args():
    parser = argparse.ArgumentParser(description='Link a git repository to a submodule, preserving history')
    parser.add_argument('--parent-branch', default=None, help='Parent branch to operate on (default: default branch after clone)')
    parser.add_argument('--submodule-name', default=None, help='Submodule name (default: last element of repo path (git default))')
    parser.add_argument('parent_repo', help='Parent repository working directory')
    parser.add_argument('submodule_repo', help='Submodule repository URI')
    return parser.parse_args()


def _git_run(cmd_str, return_output=False, env=None, **kwargs):
    check_fn = check_call
    if return_output:
        check_fn = check_output
    if debug:
        green(cmd_str.format(**kwargs))
    return check_fn(shlex.split(cmd_str.format(**kwargs)), env=env)


def _git_out(cmd_str, **kwargs):
    out = _git_run(cmd_str, return_output=True, **kwargs).strip()
    if debug:
        green('  = %s' % out)
    return out.decode('utf-8')


def inspect_repo(repo, ref=None):
    # set ref to a sha to include commits up to but not including ref
    rval = []
    for line in check_output(shlex.split("git -C {repo} log '--format=format:%H %at'".format(repo=repo))).splitlines():
        sha, stamp = line.decode('utf-8').strip().split()
        if sha == ref:
            break
        rval.append((sha, stamp))
    return list(reversed(rval))


def rev_parse(clone, abbrev_ref=False):
    return _git_out('git -C {clone} rev-parse {abbrev_ref}HEAD',
                    clone=clone,
                    abbrev_ref='--abbrev-ref ' if abbrev_ref else '')



def clone(repo, clone, branch=None):
    if not os.path.exists(clone):
        green('Cloning {repo} to {clone}'.format(repo=repo, clone=clone))
        _git_run('git clone {branch}{repo} {clone}',
                 branch='-b %s ' % branch if branch else '',
                 repo=repo,
                 clone=clone)
    elif branch:
        checkout(clone, branch)
    return rev_parse(clone=clone, abbrev_ref=True)


def checkout(clone, ref):
    _git_run('git -C {clone} checkout {ref}',
             clone=clone,
             ref=ref)


def find_submodule_commit(parent_commit, submodule_clone, submodule_ref=None):
    last_submodule_commit = ('none', -1)
    for submodule_commit in inspect_repo(submodule_clone, ref=submodule_ref):
        if submodule_commit[1] > parent_commit[1]:
            break
        last_submodule_commit = submodule_commit
    return last_submodule_commit


def find_commit_pair(parent_clone, submodule_clone, parent_ref=None, submodule_ref=None):
    # locate the oldest commit on the parent that is not older than the oldest commit on the submodule.
    oldest_submodule_commit = ('none', -1)
    for parent_commit in inspect_repo(parent_clone, ref=parent_ref):
        submodule_commit = find_submodule_commit(parent_commit, submodule_clone, submodule_ref=submodule_ref)
        if submodule_commit[1] != -1:
            return (parent_commit, submodule_commit)
    else:
        return (None, None)


def submodule_add(parent_clone, submodule_clone, submodule_repo, submodule_name):
    parent_commit, first_submodule_commit = find_commit_pair(parent_clone, submodule_clone)
    green('Adding initial submodule {name} at commit {submodule_commit} on parent commit {parent_commit}'
        .format(
            name=submodule_name,
            submodule_commit=first_submodule_commit[0],
            parent_commit=parent_commit[0]))
    # remove in case switching from a branch that has it
    #_git_run('rm -rf {clone}/{name}', clone=parent_clone, name=submodule_name)
    checkout(parent_clone, parent_commit[0])
    # --force is needed when adding it on a second branch
    _git_run('git -C {clone} submodule add --force {repo} {name}'
        .format(
            clone=parent_clone,
            repo=submodule_repo,
            name=submodule_name))
    return first_submodule_commit[0]


def submodule_update(parent_clone, submodule_clone, submodule_repo, parent_branch, submodule_name, parent_commit):
    if parent_commit:
        parent_ref = parent_commit[0]
        checkout(parent_clone, parent_ref)
        submodule_ref = find_submodule_commit(parent_commit, submodule_clone)[0]
    else:
        submodule_ref = submodule_add(parent_clone, submodule_clone, submodule_repo, submodule_name)
        parent_ref = _git_out('git -C {clone} rev-parse HEAD', clone=parent_clone)
    green('Checking out submodule {name} at commit {submodule_commit} and amending to parent commit {parent_commit}'
        .format(
            name=submodule_name,
            submodule_commit=submodule_ref,
            parent_commit=parent_ref if parent_ref else 'initial'))
    checkout('%s/%s' % (parent_clone, submodule_name), submodule_ref)
    _git_run('git -C {clone} add -- {name}',
             clone=parent_clone,
             name=submodule_name)
    _git_run('git -C {clone} commit --no-edit --amend --allow-empty-message', clone=parent_clone)
    new_ref = _git_out('git -C {clone} rev-parse HEAD', clone=parent_clone)
    new_ref_time = _git_out("git -C {clone} log '--format=format:%at' -1 {ref}", clone=parent_clone, ref=new_ref)
    checkout(parent_clone, parent_branch)
    _git_run('git -C {clone} rebase {new_commit}', clone=parent_clone, new_commit=new_ref)
    return ((new_ref, new_ref_time), submodule_ref)


if __name__ == '__main__':
    args = _parse_args()
    parent_clone = os.path.basename(args.parent_repo.rstrip('/'))
    submodule_clone = os.path.basename(args.submodule_repo.rstrip('/'))
    parent_branch = clone(args.parent_repo, parent_clone, args.parent_branch)
    clone(args.submodule_repo, submodule_clone)
    submodule_name = args.submodule_name
    if not submodule_name:
        submodule_name = os.path.basename(args.submodule_repo)
    new_commit = True
    while new_commit:
        new_commit, submodule_ref = submodule_update(parent_clone, submodule_clone, args.submodule_repo, parent_branch, submodule_name, new_commit if new_commit is not True else None)
        new_commit = find_commit_pair(parent_clone, submodule_clone, parent_ref=new_commit[0], submodule_ref=submodule_ref)[0]
    initial = _git_out('git -C {clone} rev-list --max-parents=0 HEAD', clone=parent_clone)
    _git_run("""git -C {clone} filter-branch -f --commit-filter 'export GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME"; export GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL"; export GIT_COMMITTER_DATE="$GIT_AUTHOR_DATE"; git commit-tree "$@"' -- {initial}..HEAD""", clone=parent_clone, initial=initial)
