#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remove the start and end quotes from all the files in a folder."""

import argparse
import glob
import os

def remove_quotes(dir_path):
    """Remove the start and end quotes from all the files in a folder."""
    for file in glob.glob(dir_path + "/*.json"):
        with open(file, "r") as f:
            data = f.read()
            data = data[1:-1]
            with open(file, "w") as f:
                f.write(data)


def main():
    """Main function."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir_path", type=str, default=".", help="Directory path")
    args = parser.parse_args()
    remove_quotes(args.dir_path)

if __name__ == "__main__":
    main()
