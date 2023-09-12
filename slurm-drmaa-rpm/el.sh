#!/bin/bash
set -euo pipefail

EL="$1"
TAG="slurm-drmaa-build:el$EL"

SLURM_DRMAA_VERSION='1.1.4'

SLURM_DRMAA_TARBALL="slurm-drmaa-${SLURM_DRMAA_VERSION}.tar.gz"
SLURM_DRMAA_URL="https://github.com/natefoo/slurm-drmaa/releases/download/${SLURM_DRMAA_VERSION}/${SLURM_DRMAA_TARBALL}"

[ -f "$SLURM_DRMAA_TARBALL" ] || curl -LO "$SLURM_DRMAA_URL"
[ -n "$(docker images -q $TAG)" ] || docker build -t $TAG -f Dockerfile.el$EL .

docker run --rm -it --name slurm-drmaa-build-el$EL -v $(pwd):/host $TAG /bin/bash /host/rpmbuild.sh "/host/${SLURM_DRMAA_TARBALL}" "slurm-drmaa-${SLURM_DRMAA_VERSION}/slurm-drmaa.spec"
