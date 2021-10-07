#!/usr/bin/env python3
import argparse
import json
import os
import shlex
import subprocess
import sys

import requests
import yaml


# for non-shed tools
TEST_DATA = '/home/nate/work/galaxy-test-data'


# FIXME: these args don't make sense
parser = argparse.ArgumentParser()
parser.add_argument('-g', '--galaxy', default='https://usegalaxy.org', help="Galaxy server")
parser.add_argument('-k', '--api-key', default=os.environ.get('GALAXY_API_KEY'), help="Galaxy API key")
parser.add_argument('-t', '--tool', default=None, help="Tool to list/test")
parser.add_argument('-l', '--list', action='store_true', default=False, help="List latest tool IDs from server")
parser.add_argument('-v', '--versions', action='store_true', default=False, help="List versions of tool specified in --tool")
parser.add_argument('-u', '--update', default=None, help="Update YAML file")
parser.add_argument('-p', '--process', action='store_true', default=False, help="Process test results (if tests are already run)")
parser.add_argument('-s', '--stats', action='store_true', default=False, help="Stats")
parser.add_argument('--parallel-tests', default=16)
args = parser.parse_args()


#ids = []
#elems = json.load(open(sys.argv[1]))


def api_get(tool_id=None):
    url = f"{args.galaxy}/api/tools"
    if tool_id:
        url = f"{url}?tool_id={tool_id}"
    #print(f"GET {url}", file=sys.stderr)
    r = requests.get(url)
    return r.json()


def extract_tools(ids, elems):
    for elem in elems:
        model_class = elem.get('model_class')
        if model_class.endswith('Tool'):
            ids.append(elem['id'])
        elif model_class == 'ToolSectionLabel':
            pass
        elif model_class == 'ToolSection':
            extract_tools(ids, elem['elems'])
        else:
            raise Exception(f"No unkown model class '{model_class}' in: {elem}")


def tool_versions(tool_id):
    tool_versions = []
    versions = api_get(tool_id=tool_id)
    for version in versions:
        if '/' in tool_id:
            if tool_id.rstrip('/').count('/') == 5:
                base = tool_id.rsplit('/', 1)[0]
            else:
                base = tool_id.rstrip('/')
            versioned_id = '/'.join([base, version])
            tool_versions.append(versioned_id)
        else:
            versioned_id = tool_id
            tool_versions.append(versioned_id)
            print(f"Non-shed tool {tool_id} version {version}", file=sys.stderr)
    return tool_versions


def test_dict(tool_ids):
    rval = []
    for tool_id in tool_ids:
        rval.append({
            'id': tool_id,
            'test_runs': [],
        })
    return rval


def read_yaml():
    with open(args.update) as fh:
        return yaml.safe_load(fh)


def write_yaml(yaml_tools):
    with open(args.update, 'w') as fh:
        yaml.dump(yaml_tools, fh)
        print(f"Updated {args.update}", file=sys.stderr)


def find_tool_in_list(tools, tool_id, versionless=None):
    index = None
    for i, tool_dict in enumerate(tools):
        if tool_dict['id'] == tool_id:
            return (i, True)
        elif versionless and tool_dict['id'].startswith(versionless + '/'):
            # same tool, different version
            index = i
    else:
        return (index, False)


def all_versions(tool_id):
    yaml_tools = read_yaml()
    rval = []
    for tool_dict in yaml_tools:
        if tool_dict['id'] == tool_id:
            return [tool_id]
        elif tool_dict['id'].startswith(tool_id.rstrip('/') + '/'):
            # passed in a TS id but versionless
            rval.append(tool_dict['id'])
    return rval


def add_versions_to_yaml(dicted_versions):
    yaml_tools = read_yaml()
    updated = False
    for new_tool_dict in dicted_versions:
        versionless = new_tool_dict['id'].rsplit('/', 1)[0]
        index, found = find_tool_in_list(yaml_tools, new_tool_dict['id'], versionless=versionless)
        if found:
            print(f"Tool already present in {args.update}: {new_tool_dict['id']}")
        else:
            assert index, f"No version of {versionless} found in {args.update}"
            yaml_tools.insert(index + 1, new_tool_dict)
            updated = True
    if updated:
        write_yaml(yaml_tools)


def extract_test_results(results_file):
    with open(results_file) as fh:
        results = json.load(fh)
    rval = {
        'date': None,
        'results': results['results'],
        'tests': []
    }
    for test in results['tests']:
        if not rval['date']:
            rval['date'] = test['data'].get('job', {}).get('create_time', '__FAIL__')
        rval['tests'].append({
            #'index': test['data']['test_index'],
            'status': test['data']['status'],
        })
    return rval


def get_host(url):
    return os.path.basename(url.rstrip('/'))


def get_safe_name(tool_id):
    return tool_id.replace('/', ',')


def update_test_results(tool_id, results_file):
    yaml_tools = read_yaml()
    index, found = find_tool_in_list(yaml_tools, tool_id)
    yaml_tools[index]['test_runs'].append(extract_test_results(results_file))
    write_yaml(yaml_tools)


def process_test_results(tool_id):
    # FIXME: dedup
    yaml_tools = read_yaml()
    index, found = find_tool_in_list(yaml_tools, tool_id)
    assert found, f"Tool not found in {args.update}: {tool_id}"
    host = get_host(args.galaxy)
    safe_name = get_safe_name(tool_id)
    out_dir = os.path.join(host, safe_name)
    results_file = os.path.join(out_dir, "test-results.json")
    yaml_tools[index]['test_runs'].append(extract_test_results(results_file))
    write_yaml(yaml_tools)


def test_tool(tool_id):
    assert args.api_key, "Provide an API key with -k/--api-key or $GALAXY_API_KEY"
    yaml_tools = read_yaml()
    index, found = find_tool_in_list(yaml_tools, tool_id)
    assert found, f"Tool not found in {args.update}: {tool_id}"
    host = get_host(args.galaxy)
    safe_name = get_safe_name(tool_id)
    out_dir = os.path.join(host, safe_name)
    if not os.path.exists(out_dir):
        print(f"Creating {out_dir}/", file=sys.stderr)
        os.makedirs(out_dir)
    results_file = os.path.join(out_dir, "test-results.json")
    cmd = ('galaxy-tool-test', '-k', args.api_key, '-u', args.galaxy, '--parallel-tests', str(args.parallel_tests),
           '--suite-name', tool_id, '-t', tool_id, '-o', out_dir, '-j', results_file,
           '--download-attempts', '32', '--no-history-cleanup', '--test-data', TEST_DATA)
    print(f"+ {shlex.join(cmd)}")
    try:
        subprocess.run(cmd)
        # reopen so i can write to it while running
        update_test_results(tool_id, results_file)
    except:
        update_test_results(tool_id, results_file)
        raise


def print_stats(warnings=False):
    yaml_tools = read_yaml()
    all_tools_count = len(yaml_tools)
    run_tools = list(filter(lambda x: len(x['test_runs']), yaml_tools))
    run_tools_count = len(run_tools)
    fixed_tests = 0
    broken_tests = 0
    fixed_tools = 0
    broken_tools = 0
    uninstalled_tools = 0
    for tool in run_tools:
        status = tool.get('status')
        if status == 'uninstalled':
            uninstalled_tools += 1
            continue
        elif status == 'ok':
            # forced OK because reasons
            continue
        if len(tool['test_runs']) == 1:
            if warnings:
                print(f"WARNING: only 1 test run: {tool['id']}")
            continue
        first_run_tests = tool['test_runs'][0]['tests']
        last_run_tests = tool['test_runs'][-1]['tests']
        fixed_this_tool = False
        first_run_success = False
        if len(first_run_tests) != len(last_run_tests):
            if warnings:
                print(f"WARNING: test counts do not match for tool: {tool['id']}")
            continue
        for i, first_run_test_results in enumerate(first_run_tests):
            last_run_test_results = last_run_tests[i]
            if first_run_test_results['status'] != 'success' and last_run_test_results['status'] == 'success':
                fixed_tests += 1
                fixed_this_tool = True
            elif first_run_test_results['status'] == 'success' and last_run_test_results['status'] != 'success':
                broken_tests += 1
                if warnings:
                    print(f"WARNING: broken test: {tool['id']}-{i}")
            if first_run_test_results['status'] == 'success':
                # at least one test passed originally
                first_run_success = True
        if fixed_this_tool and not first_run_success:
            fixed_tools += 1
        elif not fixed_this_tool and not first_run_success:
            if warnings:
                print(f"WARNING: tool still broken: {tool['id']}")
            broken_tools += 1
    print(f"Tests fixed: {fixed_tests}")
    print(f"Tests broken: {broken_tests}")
    print(f"Tools fixed: {fixed_tools}")
    print(f"Tools still broken: {broken_tools}")
    print(f"Tools uninstalled {uninstalled_tools}")
    print(f"{run_tools_count} of {all_tools_count} tools ({(run_tools_count/all_tools_count) * 100:0.2f}%) complete")


if args.stats:
    print_stats(warnings=True)
elif args.list:
    elems = api_get()
    tool_ids = []
    extract_tools(tool_ids, elems)
    dicted_ids = test_dict(tool_ids)
    if args.update:
        with open(args.update, 'w') as fh:
            print(yaml.dump(dicted_ids), file=fh, end='')
        print(f"Updated {args.update}", file=sys.stderr)
    else:
        print(yaml.dump(dicted_ids), end='')
elif args.versions and args.tool:
    versions = tool_versions(args.tool)
    dicted_versions = test_dict(versions)
    if args.update:
        add_versions_to_yaml(dicted_versions)
    else:
        print(yaml.dump(dicted_versions), end='')
elif args.process and args.tool:
    process_test_results(args.tool)
elif args.tool:
    # this option assumes --update
    api_versions = tool_versions(args.tool)
    dicted_versions = test_dict(api_versions)
    add_versions_to_yaml(dicted_versions)
    # this only returns a single version if you have specified a single version
    versions = all_versions(args.tool)
    for version in versions:
        print(f">>>> Testing {version}")
        test_tool(version)
    print_stats()
else:
    print("Nothing to do (hint: see --help)", file=sys.stderr)
