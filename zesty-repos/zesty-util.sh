# zesty-repos function library


#
# defaults for globals
#


function el_version() {
    local VERSION_ID
    eval $(grep ^VERSION_ID= /etc/os-release)
    echo "$VERSION_ID"
}


_RPM_DIST_SYSTEM="$(rpm --eval %{?dist})"
: "${RPM_DIST:=$_RPM_DIST_SYSTEM}"                              # e.g. .el7.centos
: "${RPM_ARCH:=$(rpm --eval %{_arch})}"                         # e.g. x86_64
: "${RPM_SUFFIX:=${RPM_DIST}.${RPM_ARCH}.rpm}"
: "${EL_VERSION:=$(el_version)}"                                # e.g. 7

: ${CREATE_BUILD_USER:=false}
: ${DEBUG:=false}

# this is actually set below at runtime since the caller may change dirs to the build dir
#: ${RPMBUILD_ROOT:=$(pwd)/rpmbuild}


#
# mostly internal stuff
#


function isintorempty() {
    # if the value referenced by the var *name* passed in $1 is:
    #   an integer: return 0
    #   empty: return 1
    #   not an integer: return 2
    # an alternate var name to use in messages can be passed in $2
    [ -n "${!1}" ] || return 1
    [ "${!1}" -eq "${!1}" ] 2>/dev/null || { rc=$?; [ $rc -ne 2 ] || { echo "WARNING: invalid non-integer value for ${2:-"\$$1"}: ${!1}" >&2; }; return $rc; }
    return 0
}


function isint() {
    # return 0 if the value referenced by the var *name* passed in $1 is an int, else return 1
    # an alternate var name to use in messages can be passed in $2
    if isintorempty $1 $2; then
        return 0
    else
        [ $? -ne 1 ] || echo "ERROR: ${2:-"\$$1"} value cannot be empty string" >&2
        return 1
    fi
}


function runas() {
    # run a command as the build user
    $DEBUG && echo "\$" "$@" >&2
    HOME="$BUILD_ROOT" su "$USER" -c '"$0" "$@"' -- "$@"
}


function log_call() {
    # call a function, log its exit, return its return (useful when there's a return in the middle of a function)
    "$@"
    local rc=$?
    $DEBUG && echo "< exited ${1} = $rc" >&2
    return $rc
}


function log_entry() {
    # log a function's entry and arguments
    $DEBUG && echo "> entered ${FUNCNAME[1]}(""$@"")" >&2
}


function log_exit() {
    # log a function's exit and arguments
    $DEBUG && echo "< exiting ${FUNCNAME[1]}(""$@"")" >&2
}


function log() {
    # log a message (to stderr)
    #
    # params:
    #   $1: log level (lowercase)
    #   $@: message
    local level="$1" ; shift
    case "$level" in
        debug)
            ! $DEBUG && return
            ;;
    esac
    printf "# %-5s: %s\n" "$level" "$@" >&2
}


function tarball_name_version() {
    # print just the name-version portion of a package tarball
    # this method works for now, wouldn't work for things where .tar does not immediately follow the version
    #
    # params:
    #   $1: tarball name in '${name}-${version}.tar*' format
    # outputs:
    #   ${name}-${version}
    echo "${1%%.tar*}"
}


function package_name_version_split() {
    # split a package name-version
    #
    # some assumptions needed to parse here since Slurm occasionally puts dashes in the patch to indicate rebuilds:
    #  1. major always starts with a number
    #  2. the final component of the name (following a hyphen) does not start with a number
    #  3. there are no '.'s in the package name
    #
    # params:
    #   $1: "package" aka ${name}-${version}
    # outputs:
    #   ${name} ${version}
    echo "$1" | sed -E 's/(^[^.]+)-([0-9].*)$/\1 \2/'
}


function package_name() {
    # print just the name portion of a package name-version
    #
    # params:
    #   $1: "package" aka ${name}-${version}
    # outputs:
    #   ${name}
    package_name_version_split "$1" | awk '{print $1}'
}


function package_version() {
    # print just the version portion of a package name-version
    #
    # params:
    #   $1: "package" aka ${name}-${version}
    # outputs:
    #   ${version}
    package_name_version_split "$1" | awk '{print $2}'
}


function fetch() {
    # fetch a tarball from a URL to the build directory using curl
    #
    # params:
    #  $1: tarball filename
    # returns:
    #  curl exit code, or 0 if the tarball already exists
    local tarball="$1"
    [ -f "$tarball" ] && return
    local package=$(tarball_name_version "$tarball")
    local url="${SRC_URLS["$package"]}"
    [ -n "$url" ] || { echo "ERROR: no URL in \$SRC_URLS for '${tarball}' (${package})" >&2 ; exit 1 ; }
    runas curl --location --output "$tarball" "$url"
}


function untar() {
    # untar a tarball in the build directory
    #
    # params:
    #  $1: tarball filename
    # returns:
    #  tar exit code, or 0 if the package source (untarred directory) already exists
    local tarball="$1"
    local package=$(tarball_name_version "$tarball")
    [ -d "$package" ] && return
    fetch "$tarball"
    runas tar xvf "$@"
}


function rpm_version_release() {
    # turn a package version in to an RPM version
    #
    # params:
    #   $1: "package" aka ${name}-${version}, where ${version} is in the format ${major}.${minor}.${patch}[-${release}]
    # globals:
    #   $RPM_BUILDS: optional hash with keys ${package} and int values of the *RPM* build id (for when you need to
    #                rebuild RPMs but the upstream version has not changed)
    # outputs:
    #   ${major}.${minor}.${patch} ${build}[.${release}]
    local package="$1"
    local _major _minor _patch _release _version _build
    read _major _minor _patch < <(package_version "$package" | awk -F. -v OFS=' ' '{print $1, $2, $3}')
    read _patch _release < <(echo "$_patch" | awk -F- -v OFS=' ' '{print $1, $2}')
    _version="${_major}.${_minor}.${_patch}"
    _build="${RPM_BUILDS[$package]:-1}"
    [ -n "$_release" ] && echo "${_version} ${_build}.${_release}" || echo "${_version} ${_build}"
}


function rpm_file() {
    # turn a package name in to an RPM filename
    #
    # params:
    #   $1: "package" aka ${name}-${version}
    # outputs:
    #   ${package}-${rpm_version}-${rpm_release}${RPM_SUFFIX}
    local package="$1"
    local name="$(package_name "$package")"
    local version release
    read version release < <(rpm_version_release "$package")
    echo "${name}-${version}-${release}${RPM_SUFFIX}"
}


function yum_dir() {
    # get the per-package yum directory (repo) of the current package/version
    #
    # globals:
    #   $REPO_NAME:     name for per-package yum repos
    #   $REPO_VERSION:  version for per-package yum repos
    #   $EL_VERSION:    major version of Enterprise Linux (e.g. 7)
    #   $RPM_ARCH:      rpm architecture (e.g. x86_64)
    # outputs:
    #   path to per-package yum repo
    echo "${YUM_ROOT}/package/${REPO_NAME}/${REPO_VERSION}/${EL_VERSION}/${RPM_ARCH}"
}


function check_repo_package() {
    # check per-package yum directory (both repo and staging paths) for the given package (rpm)
    #
    # params:
    #   $1: "package" aka ${name}-${version}
    # returns:
    #   0 if rpm for package is found, else 1
    local package="$1"
    local rpm="$(rpm_file "$package")"
    local yum="$(yum_dir)"
    [ -f "${yum}/${rpm}" -o -f "${yum}/_staging/${rpm}" ]
}


function build_rpm() {
    # build an rpm of a package
    #
    # requires:
    #   ${package_name}.spec exists at the root of the package directory of the tarball
    # params:
    #   $1: tarball filename
    # globals:
    #   $RPMBUILD_ROOT: rpmbuild root directory
    #   $RPM_ARCH:      rpm architecture (e.g. x86_64)
    log_entry "$@"
    local tarball="$1"
    local package=$(tarball_name_version "$tarball")
    local specfile="$(package_name "$package").spec"
    local topdir="${RPMBUILD_ROOT:=$(pwd)/rpmbuild}/${package}"
    local version release
    read version release < <(rpm_version_release "$package")

    # return if already built
    [ -f "${topdir}/RPMS/${RPM_ARCH}/$(rpm_file "$package")" ] && return

    # set up rpmbuild
    runas mkdir -p "${topdir}"/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
    # untar fetches if needed
    untar "$tarball" --strip-components=1 -C "${topdir}/SPECS" "${package}/${specfile}"
    [ -f "${topdir}/SOURCES/${tarball}" ] || runas cp "$tarball" "${topdir}/SOURCES"
    # override release; %rel is only used in the spec for slurm 17.11 and later
    sed -i -e "s/^\(Release:\s*\).*$/\\1${release}%{?dist}/" "${topdir}/SPECS/${specfile}"

    # install rpmbuild and development deps
    yum install -y rpm-build '@development tools'
    yum-builddep -y "${topdir}/SPECS/${package%%-*}.spec"

    # build
    if [ "$RPM_DIST" != "$_RPM_DIST_SYSTEM" ]; then
        runas rpmbuild --define "_topdir ${topdir}" --define "dist ${RPM_DIST}" -ba "${topdir}/SPECS/${specfile}"
    else
        runas rpmbuild --define "_topdir ${topdir}" -ba "${topdir}/SPECS/${specfile}"
    fi
    log_exit
}


function stage_rpm() {
    # stage rpms from the rpmbuild directory to the staging directory of the per-package yum repo, building if needed
    #
    # params:
    #   $1: tarball filename
    # globals:
    #   $RPMBUILD_ROOT: rpmbuild root directory
    log_entry "$@"
    local tarball="$1"
    local package=$(tarball_name_version "$tarball")
    local topdir="${RPMBUILD_ROOT:=$(pwd)/rpmbuild}/${package}"
    local staging="$(yum_dir)/_staging"

    # skip if already staged
    local rpm="$(rpm_file "$package")"
    [ -f "${staging}/${rpm}" ] && continue

    # build if needed
    build_rpm "$tarball"

    # stage
    runas mkdir -p "$staging"
    runas cp -p "${topdir}"/RPMS/${RPM_ARCH}/*.rpm "$staging"
    log_exit
}


function find_rpm() {
    # locates an rpm matching the given name in the given dir, ignoring version
    #
    # params:
    #   $1: package name of rpm to find
    #   $2: directory to search
    # outputs:
    #   unqualified filename of matching rpm in $dir
    # returns:
    #   0 if matching rpm is found, otherwise 1
    local name="$1"
    local dir="$2"
    local rpm
    for rpm in "${dir}"/${name}*.rpm; do
        [ "$rpm" == "${dir}/${name}*.rpm" ] && break   # no rpms in dir
        local _name="$(rpm --queryformat '%{NAME}' -qp "$rpm")"
        if [ "$name" == "$_name" ]; then
            echo "$(basename "$rpm")"
            return 0
        fi
    done
    return 1
}


function archive_rpm() {
    # archive an rpm in a yum repo to the _archive directory
    #
    # params:
    #   $1: unqualified pathname of rpm to archive
    #   $2: yum repo
    local rpm="$1"
    local dir="$2"
    [ -z "$rpm" ] && return     # find_rpm output nothing
    runas mkdir -p "${dir}/_archive"
    runas mv "${dir}/${rpm}" "${dir}/_archive"
    log info "Archived ${rpm} to ${dir}/_archive"
}


function deploy_rpm() {
    # deploy staged rpm to repo
    #
    # params:
    #   $1: unqualified pathname of rpm to deploy
    #   $2: yum repo
    local rpm="$1"
    local dir="$2"
    runas mv "${dir}/_staging/${rpm}" "$dir"
    log info "Deployed ${rpm} to ${dir}"
}


#
# public stuff
#


function deploy_repo_file() {
    # generate a yum .repo file in a per-package yum repository
    #
    # creates ${name}-${major}.${minor}.repo in ${REPO_NAME/${REPO_VERSION} and symlinks ${name}.repo to it
    #
    # globals:
    #   $REPO_NAME:     name for per-package yum repos
    #   $REPO_VERSION:  version for per-package yum repos
    log_entry "$@"
    local dir="${YUM_ROOT}/package/${REPO_NAME}/${REPO_VERSION}"
    local repo_file="${dir}/${REPO_NAME}-${REPO_VERSION}.repo"
    if [ ! -f "$repo_file" ]; then
        tmp="$(mktemp zesty-repo-XXXXXXXX)"
        cat >"$tmp" <<EOF
[${REPO_NAME}-${REPO_VERSION}]
name=Galaxy ${REPO_NAME} ${REPO_VERSION} packages \$releasever - \$basearch
baseurl=${YUM_URL_ROOT}/yum/${REPO_NAME}/${REPO_VERSION}/el/\$releasever/\$basearch/
enabled=1
gpgcheck=0
EOF
        chmod 644 "$tmp"
        runas cp "$tmp" "$repo_file"
        rm "$tmp"
    fi
    [ ! -e "${dir}/${REPO_NAME}.repo" ] && runas ln -s "${REPO_NAME}-${REPO_VERSION}.repo" "${dir}/${REPO_NAME}.repo"
    log_exit
}


function deploy_repo_to_gpel() {
    # deploy to GPEL if this is the "current" version of the package
    #
    # params:
    #   $@: unqualified pathnames of rpms in per-package yum repo to deploy to gpel
    # globals:
    #   $REPO_NAME:     name for per-package yum repos
    #   $REPO_VERSION:  version for per-package yum repos
    #   $YUM_GPEL:      path to gpel yum repo
    log_entry "$@"
    local staged=("$@")
    local current="${YUM_ROOT}/package/${REPO_NAME}/current"
    [ -n "$YUM_GPEL" ] || return
    local dir="$(yum_dir)"
    local rpm
    if [ -h "$current" -a "$(readlink "$current")" == "$REPO_VERSION" ]; then
        # this repo is pointed to by the 'current' symlink
        runas mkdir -p "${YUM_GPEL}"/{_staging,_archive}
        for rpm in "${staged[@]}"; do
            runas cp -p "${dir}/$(basename "$rpm")" "${YUM_GPEL}/_staging"
        done
        deploy_repo "$YUM_GPEL"
    fi
    log_exit
}


function deploy_repo() {
    # deploy staged packages to yum repo
    #
    # if $YUM_GPEL is set and this is the "current" version, it will also be deployed to GPEL (see deploy_repo_to_gpel)
    #
    # params:
    #   $1: optional path to repo to deploy, defaults to per-package repository defined by $REPO_NAME and $REPO_VERSION
    # globals:
    #   $REPO_NAME:     name for per-package yum repos
    #   $REPO_VERSION:  version for per-package yum repos
    log_entry "$@"
    local dir="$1"
    local rpm
    [ -z "$dir" ] && dir="$(yum_dir)"

    # snapshot of what's in staging for gpel deployment
    local staged=("${dir}"/_staging/*.rpm)

    for rpm in ${staged[@]}; do
        [ "$rpm" == "${dir}/_staging/*.rpm" ] && return   # no rpms in staging
        rpm="$(basename "$rpm")"

        # archive older versions
        local _name="$(rpm --queryformat '%{NAME}' -qp "${dir}/_staging/${rpm}")"
        archive_rpm "$(find_rpm "$_name" "$dir")" "$dir"

        # deploy
        deploy_rpm "$rpm" "$dir"
    done
    # generate yum metadata
    yum install -y createrepo
    runas createrepo -v "$dir"
    # deploy to GPEL if desired
    [ -z "$1" ] && deploy_repo_to_gpel "${staged[@]}"
    log_exit
}


function install_rpm() {
    # install rpm(s), e.g. as a build dependency
    #
    # requires:
    #   rpm(s) to exist in per-package repo (or staging)
    # params:
    #   $1: "package" aka ${name}-${version}
    # globals:
    #   $RPM_DEPS: optional hash with keys ${package} and string values indicating the *name* of a global containing an
    #              array of packages in the per-package repo that must be installed along with ${package}
    #   $REPO_NAME:     name for per-package yum repos
    #   $REPO_VERSION:  version for per-package yum repos
    log_entry "$@"
    local package="$1"
    local name="$(package_name "$package")"

    # return if already installed
    rpm -q "$name" >/dev/null && return

    local yum="$(yum_dir)"
    local rpms=()
    local dep

    # indirect reference for reading an array whose variable name is stored in ${RPM_DEPS["$package"]}
    local deps_array_ind=${RPM_DEPS["$package"]}[@]
    # convert deps to rpm filenames
    for dep in "$package" "${!deps_array_ind}"; do
        local dir=
        local rpm="$(rpm_file "$dep")"
        if [ -f "${yum}/${rpm}" ]; then
            dir="$yum"
        elif [ -f "${yum}/_staging/${rpm}" ]; then
            dir="${yum}/_staging"
        else
            echo "ERROR: Cannot find RPM: ${rpm}" >&2
            exit 1
        fi
        rpms+=("${dir}/${rpm}")
    done
    # install
    rpm -Uv "${rpms[@]}"
    log_exit
}


function uninstall_rpm() {
    # uninstall rpm(s)
    #
    # allows for multiple builds in one session
    #
    # params:
    #   $1: "package" aka ${name}-${version}
    # globals:
    #   $RPM_DEPS: optional hash with keys ${package} and string values indicating the *name* of a global containing an
    #              array of packages in the per-package repo that must be installed along with ${package}
    log_entry "$@"
    local package="$1"
    local name="$(package_name "$package")"

    # return if already uninstalled
    ! rpm -q "$name" >/dev/null && return

    local names=()
    local dep

    # indirect reference for reading an array whose variable name is stored in ${RPM_DEPS["$package"]}
    local deps_array_ind=${RPM_DEPS["$package"]}[@]
    # convert deps to package names
    for dep in "$package" "${!deps_array_ind}"; do
        names+=("$(package_name "$dep")")
    done
    # uninstall
    rpm -e "${names[@]}"
    log_exit
}


function install_jq() {
    # fetch a copy of jq
    #
    # useful for parsing github api output
    #
    # globals:
    #   $JQ: path to JQ if already installed (skips fetching)
    # sets:
    #   $JQ: path to JQ if unset
    log_entry
    if [ ! -f 'jq' -a -z "$JQ" ]; then
        curl --location --output jq "https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux64"
        chmod +x jq
    fi
    [ -z "$JQ" ] && JQ="./jq"
    log_exit
}


function create_build_user() {
    # create a build user
    #
    # this utility is meant to be run inside virtualization with the yum repo(s) mounted as a volume, this ensures that
    # the user building and deploying the rpms is the same as the volume's owner
    #
    # globals:
    #   $CREATE_BUILD_USER: set to 'true' if a user should be created, default is 'false'
    #   $BUILD_USER_FROM: path which the build user's UID and GID should be determined (the owner of the path)
    log_entry
    # also creates $BUILD_ROOT if needed
    ! $CREATE_BUILD_USER && return
    local uid gid user group
    read uid gid < <(stat --format='%u %g' "$BUILD_USER_FROM")
    group=$(getent group $gid) && GROUP=${group%%:*} || groupadd -g $gid $GROUP
    user=$(getent passwd $uid) && USER=${user%%:*} || useradd -u $uid -g $gid -s /bin/bash -m -d "$BUILD_ROOT" $USER
    log_exit
}
