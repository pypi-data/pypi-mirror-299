#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hakkero.dataset.iterable_dataset import IterableDataset

if __name__ == "__main__":
    ds = IterableDataset(
        path="hermes25",
        name="hermes25",
        seed=-1,
        max_epoch=1,
        block_size=8192,
        n_shards=1,
        rank=0,
        world_size=1
    )

    for i, d in enumerate(ds):
        print(f"i={i}")
