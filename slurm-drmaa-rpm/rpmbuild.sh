#!/bin/bash
set -euo pipefail

rpms_dir="/host/rpms-$(hostname)"
chown_arg=$(stat --printf "%u:%g" /host)

set -x
mkdir -p "$HOME"/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
cp "$1" "$HOME/rpmbuild/SOURCES"
tar xvf "$1" --strip-components=1 -C "${HOME}/rpmbuild/SPECS" "$2"

rpmbuild -ba "$HOME/rpmbuild/SPECS/$(basename $2)"

mkdir $rpms_dir
cp $HOME/rpmbuild/RPMS/x86_64/*.rpm $rpms_dir
chown -Rh $chown_arg $rpms_dir
