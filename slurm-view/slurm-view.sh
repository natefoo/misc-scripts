#!/bin/bash
#
# TODO:
#
# - any way to calculate slots in a nonspecific manner?
# - don't hardcode def_mem_per_cpu?
# - calculations are wrong for mslots
# - slots stats are not useful enough. you need:
#   - number of slots running out of current partition size
#   - number of slots running on nodes not in current partition (due to resizing)

def_mem_per_cpu=7680

function count_slots() {
    partition=$1
    local slots used total_slots
    local mem_per_node nodect

    # collect data
    read mem_per_node nodect < <(sinfo -p $partition -h -o "%m %D")
    squeue_out=$(squeue -p $partition -h --noconvert -o "%t %m" | sort | uniq -c)

    total_slots=$((nodect * $mem_per_node / $def_mem_per_cpu))

    while read ct status mem; do
        slots=$(((($def_mem_per_cpu - 1 + ${mem/M/}) / $def_mem_per_cpu) * $ct))
        [ $status = "R" ] && used=$((used + $slots))
    done <<< "$squeue_out"

    # second loop is needed because piping to column results in a subshell that can't modify $used for the summary
    {
        printf "JOBS SLOTS MEMSIZE STATUS\n"
        while read ct status mem; do
        slots=$(((($def_mem_per_cpu - 1 + ${mem/M/}) / $def_mem_per_cpu) * $ct))
        printf "%s %s %s %s\n" $ct $slots $((${mem/M/} / 1024))G $status
    done <<< "$squeue_out" ; } | column -t
    printf "\nUsing %s of %s slots in $partition partition\n" $used $total_slots
}

function _partition_arg() {
    case $1 in
        '')
            : #noop
            ;;
        *)
            printf -- "-p %s" "$1"
            ;;
    esac
}

function _clusters_arg() {
    case $1 in
        multi)
            printf -- "-M roundup,jetstream-tacc,jetstream-iu"
            ;;
    esac
}


function pd_count() {
    local partition_arg=$(_partition_arg $1)
    local clusters_arg=$(_clusters_arg $1)
    local pdct=0
    while read jobid; do
        case $jobid in
            ''|CLUSTER:*)
                : # noop
                ;;
            *)
                pdct=$((pdct + 1))
                ;;
        esac
    done < <(squeue $partition_arg $clusters_arg -t PD -h -o "%i")
    printf "Total pending jobs: $pdct\n"
}


function slurm_queue() {
    local partition_arg=$(_partition_arg $1)
    local clusters_arg=$(_clusters_arg $1)
    local output_arg
    case $1 in
        multi)
            output_arg="-o %.10i %.8u %.2t %.10M %.7m %.3C %24R %j"
            ;;
        *)
            output_arg="-o %.10i %.8u %.2t %.10M %.7m %.3C %16R %j"
            ;;
    esac
    squeue $partition_arg $clusters_arg "$output_arg"
    printf "\n"
    pd_count $1
    printf "\n"
}


function slurm_node_info() {
    local partition_arg=$(_partition_arg $1)
    local clusters_arg=$(_clusters_arg $1)
    local local_args="-Ne"
    local output_arg
    width=$(sinfo $partition_arg $clusters_arg $local_args -h -o "%N" | wc -L)
    case $1 in
        '')
            : # noop
            ;;
        *)
            output_arg="-o %.${width}N %.6D %.11T %.8e %.6m %.13C %.6O %20E"
            ;;
    esac
    sinfo $partition_arg $clusters_arg $local_args "$output_arg"
}


case $1 in
    nslots)
        count_slots normal
        ;;
    mslots)
        count_slots multi
        ;;
    nq)
        slurm_queue normal
        ;;
    mq)
        slurm_queue multi
        ;;
    q)
        slurm_queue
        ;;
    ni)
        slurm_node_info normal
        ;;
    mi)
        slurm_node_info multi
        ;;
    *)
        echo "usage: sutil <{n,m}slots|{n,m}q|{n,m}i>"
        exit 2
        ;;
esac
