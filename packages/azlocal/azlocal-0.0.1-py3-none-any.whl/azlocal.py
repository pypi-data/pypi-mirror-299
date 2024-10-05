#!/usr/bin/env python

"""
Thin wrapper around the "az" command line interface (CLI) for use
with LocalStack.

The "azlocal" CLI allows you to easily interact with your local Azure services
without having to configure anything.

Example:
Instead of the following command ...
HTTPS_PROXY=... REQUESTS_CA_BUNDLE=... az storage account list
... you can simply use this:
az storage account list

Options:
  Run "azlocal help" for more details on the Azure CLI subcommands.
"""

import os
import shutil
import sys
from pathlib import Path


def usage():
    print(__doc__.strip())


def run(cmd, env):
    """
    Replaces this process with the AZ CLI process, with the given command and environment
    """
    os.execvpe(cmd[0], cmd, env)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '-h':
        return usage()
    run_as_separate_process()


def check_proxy_is_running():
    pass
    # TODO: use internal health endpoint once https://github.com/localstack/localstack-ext/pull/3465 is merged


def prepare_environment():

    home_dir = Path.home()
    azure_config_dir = os.path.join(home_dir, ".localstack/azure")

    if not os.path.exists(azure_config_dir):
        Path(azure_config_dir).mkdir(parents=True, exist_ok=True)

    certificate_path = os.path.join(azure_config_dir, "ca.crt")
    if not os.path.exists(certificate_path):
        # TODO: Download from Proxy, once it's exposed?
        shutil.copyfile("ca.crt", dst=certificate_path)

    # prepare env vars
    env_dict = os.environ.copy()

    env_dict['HTTP_PROXY'] = 'http://localhost:4566'
    env_dict['HTTPS_PROXY'] = 'http://localhost:4566'
    env_dict['REQUESTS_CA_BUNDLE'] = certificate_path

    # update environment variables in the current process
    os.environ.update(env_dict)

    return env_dict


def run_as_separate_process():
    """
    Constructs a command line string and calls "az" as an external process.
    """
    check_proxy_is_running()

    env_dict = prepare_environment()

    cmd_args = list(sys.argv)
    cmd_args[0] = 'az'

    # Hijack the login command to automatically login
    if len(cmd_args) > 1 and cmd_args[1] == "login" and "--help" not in cmd_args:
        cmd_args = ["az", "login", "--service-principal", "-u", "any-app", "-p", "any-pass", "--tenant", "any-tenant"]

    # run the command
    run(cmd_args, env_dict)


if __name__ == '__main__':
    main()
