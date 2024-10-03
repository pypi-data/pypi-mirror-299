#!/usr/bin/env python
# -*- coding: utf-8 -*-

from transformers import AutoTokenizer

from hakkero.dataset import UnpadLoader, PadLoader
from hakkero.dataset.mixed_dataset import get_dataset


if __name__ == "__main__":
    config = {
        "openids": {
            "group": "en",
            "name": "openids",
            "epoch": 1,
            "path": "openids",
            "strategy": {
                "st_segment": "integrous",
                "st_tokenize": "hg"
            },
            "weight": 1.0,
        }
    }

    model_path = "/Users/qinluo/work/models/Qwen/Qwen2-7B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

    max_length = 4096
    batch_size = 1
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

    # dataloader = UnpadLoader(ds, max_total_length=batch_size * max_length)
    dataloader = PadLoader(ds, batch_size=batch_size, padding_id=tokenizer.pad_token_id)

    total_samples = 0
    for step, batch in enumerate(dataloader, start=1):
        total_samples += batch['n_samples']
        print(f"step={step}, samples={batch['n_samples']}, total_samples={total_samples}")

