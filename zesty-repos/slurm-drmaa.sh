#!/bin/bash
set -eo pipefail

# build slurm-drmaa

# prevents fetching if things already exist, sets -x, etc.
: ${DEVMODE:=false}
# debug logging
: ${DEBUG:=true}

$DEVMODE && set -x

# default on centos is .el7.centos
RPM_DIST=.el7

# RPM Build numbers
declare -A RPM_BUILDS
# default is 1, to force a new RPM build, increment like so (e.g.):
#RPM_BUILDS['munge-0.5.13']=2

BUILD_ROOT=/build

declare -A RPM_DEPS
declare -A SRC_URLS

# set $JQ to avoid downloading JQ every time

SLURM_DRMAA_RELEASE_URL='https://api.github.com/repos/natefoo/slurm-drmaa/releases/latest'
SLURM_DRMAA_VERSION=
SLURM_DRMAA_TARBALL=

YUM_ROOT='/yum'
YUM_URL_ROOT='https://depot.galaxyproject.org/yum'

CREATE_BUILD_USER=true
BUILD_USER_FROM="$YUM_ROOT"
USER=build
GROUP=build

REPO_NAME='slurm'
REPO_VERSION=


# include library
. "$(dirname "$0")/zesty-util.sh"


YUM_GPEL="${YUM_ROOT}/el/${EL_VERSION}/${RPM_ARCH}"


function current_slurm_repo_versions() {
    # TODO: at some point we will need a way to limit the minimum Slurm version that Slurm DRMAA should be built for, or
    # maybe just move older slurm versions to an archive.
    for _version in "${YUM_ROOT}/package/${REPO_NAME}/"*.*; do
        _version=$(basename  $_version)
        read _major _minor < <(echo "$_version" | awk -F. -v OFS=' ' '{print $1, $2}')
        isint _major && isint _minor || continue
        echo "${_major}.${_minor}"
    done
}


function set_slurm_drmaa_facts() {
    local _slurm_version="$1"
    if [ -z "$SLURM_DRMAA_VERSION" ]; then
        SLURM_DRMAA_VERSION="$(curl --silent "$SLURM_DRMAA_RELEASE_URL" | "$JQ" --raw-output '.tag_name')"
        SLURM_DRMAA_TARBALL="slurm-drmaa-${SLURM_DRMAA_VERSION}.tar.gz"
        SRC_URLS["slurm-drmaa-${SLURM_DRMAA_VERSION}"]="https://github.com/natefoo/slurm-drmaa/releases/download/${SLURM_DRMAA_VERSION}/${SLURM_DRMAA_TARBALL}"
    fi
}


function check_slurm_drmaa_for_slurm_version() {
    log_entry "$@"
    local _slurm_version="$1"
    set_slurm_drmaa_facts "${_slurm_version}"
    log info "slurm-drmaa latest stable: ${SLURM_DRMAA_VERSION}"
    local package="$(tarball_name_version "$SLURM_DRMAA_TARBALL")"
    check_repo_package "$package" && { log info "$package already staged or deployed in ${REPO_NAME}/${REPO_VERSION}"; return; }
    yum_install_package "slurm-${_slurm_version}"
    yum_install_package "slurm-devel-${_slurm_version}"
    stage_rpm "slurm-drmaa-${SLURM_DRMAA_VERSION}.tar.gz"
    yum_uninstall_package "slurm-devel-${_slurm_version}"
    yum_uninstall_package "slurm-${_slurm_version}"
}


function check_slurm_drmaa() {
    # build all current versions of slurm
    install_jq
    local version
    for version in $(current_slurm_repo_versions); do
        REPO_VERSION="${version}"

        # ensure slurm-drmaa is up to date
        check_slurm_drmaa_for_slurm_version "$version"

        # deploy staging to repo
        deploy_repo
        deploy_repo_file
    done
}


function main() {
    log_entry
    create_build_user
    cd ${BUILD_ROOT}

    # build slurm-drmaa for all current versions of slurm
    check_slurm_drmaa
    log_exit
}


main
