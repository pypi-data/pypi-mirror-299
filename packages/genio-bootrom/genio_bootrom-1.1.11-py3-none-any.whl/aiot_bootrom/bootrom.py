# SPDX-License-Identifier: MIT
# Copyright 2021 (c) BayLibre, SAS
# Author: Fabien Parent <fparent@baylibre.com>

from importlib import resources
import platform
import subprocess
import sys

def main():
    run(sys.argv)

def run(argv):
    """
    Locate the pre-built binary 'bootrom-tool' for x64/aarch64 Windows &
    Linux, and execute it to communicate with Genio SoC boot ROM via USB.
    """
    mach = platform.machine().lower()
    system = platform.system().lower()
    bin_name = f'bin/{mach}/{system}/bootrom-tool'
    if platform.system() == "Windows":
        bin_name += ".exe"

    exe_path = resources.files('aiot_bootrom') / bin_name
    with resources.as_file(exe_path) as binary:
        argv[0] = binary
        try:
            subprocess.run(argv, check=True)
        except KeyboardInterrupt:
            pass

