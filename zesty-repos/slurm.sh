#!/bin/bash
set -eo pipefail

# build slurm and friends (munge, slurm-drmaa)

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

MUNGE_RELEASE_URL='https://api.github.com/repos/dun/munge/releases/latest'
MUNGE_VERSION=
MUNGE_TARBALL=
MUNGE_DEPS=()

SLURM_URL='https://download.schedmd.com/slurm'
SLURM_SHA="${SLURM_URL}/SHA1"
SLURM_DEPS=()

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


function sha_file() {
    { ! $DEVMODE || [ ! -f "${SLURM_SHA##*/}" ]; } && curl --remote-name "$SLURM_SHA"
    cat "${SLURM_SHA##*/}"
}


function latest_slurm_tarballs() {
    major=-1
    minor=-1
    latest=
    for tb in $(sha_file | awk '{print $NF}' | sort -V | xargs echo); do
        read _major _minor _patch < <(echo "$tb" | sed 's/^slurm-//' | awk -F. -v OFS=' ' '{print $1, $2, $3}')
        read _patch _build < <(echo "$_patch" | awk -F- -v OFS=' ' '{print $1, $2}')
        isint _major && isint _minor && isint _patch && { isintorempty _build || [ $? -eq 1 ] && true; } || continue
        if [ $major -eq -1 ]; then
            major=$_major
            minor=$_minor
        fi
        if [ $_major -eq $major -a $_minor -eq $minor ]; then
            latest="$tb"
        else
            echo "$latest"
            log info "slurm ${major}.${minor} latest stable: ${latest}"
            major=$_major
            minor=$_minor
        fi
    done
    echo "$latest"
    log info "slurm ${major}.${minor} latest stable: ${latest}"
}


function set_munge_facts() {
    # munge currently tags releases as 'munge-X.Y.Z'
    local _package="$(curl --silent "$MUNGE_RELEASE_URL" | "$JQ" --raw-output '.tag_name')"
    MUNGE_VERSION="${_package##*-}"
    MUNGE_TARBALL="munge-${MUNGE_VERSION}.tar.xz"
    MUNGE_DEPS+=("munge-libs-${MUNGE_VERSION}" "munge-devel-${MUNGE_VERSION}")
    SRC_URLS["munge-${MUNGE_VERSION}"]="https://github.com/dun/munge/releases/download/munge-${MUNGE_VERSION}/${MUNGE_TARBALL}"
    RPM_DEPS["munge-${MUNGE_VERSION}"]='MUNGE_DEPS'
}


function check_munge() {
    install_jq
    set_munge_facts
    log info "munge latest stable: ${MUNGE_VERSION}"
    local package="$(tarball_name_version "$MUNGE_TARBALL")"
    check_repo_package "$package" && { log info "$package already staged or deployed in ${REPO_NAME}/${REPO_VERSION}"; return; }
    # build new version of munge if needed
    stage_rpm "$MUNGE_TARBALL"
}


function slurm_build_setup() {
    local package=$(tarball_name_version "$MUNGE_TARBALL")
    install_rpm "$package"
    yum install -y mariadb-devel    # not listed as a slurm build dep
}


function set_slurm_drmaa_facts() {
    local _slurm_version="$1"
    if [ -z "$SLURM_DRMAA_VERSION" ]; then
        SLURM_DRMAA_VERSION="$(curl --silent "$SLURM_DRMAA_RELEASE_URL" | "$JQ" --raw-output '.tag_name')"
        SLURM_DRMAA_TARBALL="slurm-drmaa-${SLURM_DRMAA_VERSION}.tar.gz"
        SRC_URLS["slurm-drmaa-${SLURM_DRMAA_VERSION}"]="https://github.com/natefoo/slurm-drmaa/releases/download/${SLURM_DRMAA_VERSION}/${SLURM_DRMAA_TARBALL}"
    fi
    case "$REPO_VERSION" in
        17.02)
            SLURM_DEPS=("slurm-devel-${_slurm_version}" "slurm-plugins-${_slurm_version}" "munge-${MUNGE_VERSION}" "munge-libs-${MUNGE_VERSION}")
            ;;
        *)
            SLURM_DEPS=("slurm-devel-${_slurm_version}" "munge-${MUNGE_VERSION}" "munge-libs-${MUNGE_VERSION}")
            ;;
    esac
    RPM_DEPS["slurm-${_slurm_version}"]='SLURM_DEPS'
}


function check_slurm_drmaa() {
    local _slurm_version="$1"
    install_jq
    set_slurm_drmaa_facts "${_slurm_version}"
    log info "slurm-drmaa latest stable: ${SLURM_DRMAA_VERSION}"
    local package="$(tarball_name_version "$SLURM_DRMAA_TARBALL")"
    check_repo_package "$package" && { log info "$package already staged or deployed in ${REPO_NAME}/${REPO_VERSION}"; return; }
    yum install -y mariadb-libs
    install_rpm "slurm-${_slurm_version}"
    stage_rpm "slurm-drmaa-${SLURM_DRMAA_VERSION}.tar.gz"
    uninstall_rpm "slurm-${_slurm_version}"
}


function check_slurm() {
    # build all current versions of slurm
    log_entry "$@"
    local tarball
    for tarball in $(latest_slurm_tarballs); do
        # set repo path
        local package="$(tarball_name_version "$tarball")"
        local version="$(package_version "$package")"
        local _major _minor
        read _major _minor < <(echo "$version" | awk -F. -v OFS=' ' '{print $1, $2}')
        REPO_VERSION="${_major}.${_minor}"
        SRC_URLS["$package"]="${SLURM_URL}/${tarball}"

        # ensure munge is up to date
        check_munge

        # ensure slurm is up to date
        if ! check_repo_package "$package"; then
            log_call slurm_build_setup
            stage_rpm "$tarball"
        else
            log info "$package already staged or deployed in ${REPO_NAME}/${REPO_VERSION}"
        fi

        # to avoid conflicts attempting to install munge as a slurm-drmaa dep (rpm fails if it's already installed)
        uninstall_rpm "munge-${MUNGE_VERSION}"

        # ensure slurm-drmaa is up to date
        check_slurm_drmaa "$version"

        # deploy staging to repo
        deploy_repo
        deploy_repo_file
    done
}


function main() {
    log_entry
    create_build_user
    cd ${BUILD_ROOT}

    # build all current versions of slurm
    check_slurm
    log_exit
}


main
