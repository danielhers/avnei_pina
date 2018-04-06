#!/usr/bin/python3
import os
import sys
from glob import glob

from pyexcel.cookbook import merge_all_to_a_book
from tqdm import tqdm


def all_files():
    for pattern in sys.argv[1:]:
        yield from glob(pattern) or pattern


for filename in tqdm(list(all_files()), desc="Converting files", unit="file"):
    basename, _ = os.path.splitext(filename)
    merge_all_to_a_book([filename], basename + ".xlsx")
