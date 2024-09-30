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
    ds = get_dataset(
        config,
        tokenizer,
        num_epochs=1,
        max_length=1024,
        homogeneous=True,
        seed=-1,
        rank=0,
        world_size=1,
        n_workers=1
    )

    for i, d in enumerate(ds):
        print(f"i={i}")

