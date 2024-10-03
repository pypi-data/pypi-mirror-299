#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hakkero.dataset.indexed_dataset import IndexedDataset

if __name__ == "__main__":
    ds = IndexedDataset("openids")
    print(len(ds))
    for i, d in enumerate(ds):
        print(f"i={i}, d={d}")
