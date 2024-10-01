#!/usr/bin/env python
# -*- coding: utf-8 -*-

from transformers import AutoTokenizer

from hakkero.dataset import UnpadLoader
from hakkero.dataset.mixed_dataset import get_dataset


if __name__ == "__main__":
    config = {
        "hermes25_1": {
            "group": "en",
            "name": "hermes25_1",
            "epoch": 1,
            "path": "hermes25",
            "recipe": {
                "segment": "integrous",
                "tokenize": "hg"
            },
            "weight": 0.5,
        },
        "hermes25_2": {
            "group": "en",
            "name": "hermes25_1",
            "epoch": 1,
            "path": "hermes25",
            "recipe": {
                "segment": "integrous",
                "tokenize": "hg"
            },
            "weight": 0.5,
        }
    }

    model_path = "/Users/qinluo/work/models/Qwen/Qwen2-7B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

    max_length = 4096
    batch_size = 4
    n_workers = 2

    ds = get_dataset(
        config,
        tokenizer,
        num_epochs=1,
        max_length=max_length,
        homogeneous=True,
        seed=-1,
        rank=0,
        world_size=1,
        n_workers=n_workers
    )

    dataloader = UnpadLoader(ds, max_total_length=batch_size * max_length)
    prefetcher = dataloader.prefetch(n_workers)

    for step, batch in enumerate(prefetcher, start=1):
        print(step)

