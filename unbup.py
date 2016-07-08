#!/usr/bin/env python3

import os
import sys
import subprocess

HELP="""Unbup: extract BUP McAfee quarantine files

Usage: unbup [-h] FILE...

Options:
    -h, --help      Print this help and exit

Arguments:
    FILE            Files to recover
"""

def main():
    if len(sys.argv) == 1:
        print(HELP)
        return 1;

    if "-h" in sys.argv or "--help" in sys.argv:
        print(HELP)
        return 0;

    for arg in sys.argv[1:]:
        filepath = os.path.abspath(os.path.expanduser(arg))
        filename = os.path.basename(filepath)
        os.mkdir(filename + "_unbup")
        os.chdir(filename + "_unbup")
        os.rename(filepath, filename)

        try:
            p = subprocess.Popen(["7z", "x", filename])
            p.wait()
        except FileNotFoundError as e:
            print("Please, make sure that 7z is installed", file=sys.stdout)

        for each in ["Details", "File_0"]:
            with open(each, "rb") as fin:
                with open(each + ".tmp", "wb") as fout:
                    fout.write(bytes(map(lambda x: x ^ 0x6A, fin.read())))
            os.rename(each + ".tmp", each)

        os.chdir("..")

if __name__ == "__main__":
    main()
