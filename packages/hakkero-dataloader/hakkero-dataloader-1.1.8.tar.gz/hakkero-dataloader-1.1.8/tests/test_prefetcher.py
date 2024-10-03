#!/usr/bin/env python
# -*- coding: utf-8 -*-

from transformers import AutoTokenizer

from hakkero.dataset import UnpadLoader, PadLoader
from hakkero.dataset.mixed_dataset import get_dataset


if __name__ == "__main__":
    config = {
      "openhermes25": {
        "group": "en_general",
        "name": "en_general",
        "epoch": 1,
        "path": "/ckenfs/pvc-46a3ae43-9539-4abb-a4ae-2f526f410730/hairuo-zero/cookbooks/debug/data/debug100",
        "strategy": {
          "st_segment": "integrous",
          "st_tokenize": "hg"
        },
        "weight": 1.0
      }
    }

    model_path = "/ckenfs/pvc-fad5e435-2f6a-4b26-b51d-15113d747234/Qwen2.5-1.5B"
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

    max_length = 8192
    batch_size = 1
    n_workers = 1

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

    # dataloader = PadLoader(ds, max_total_length=batch_size * max_length)
    dataloader = PadLoader(ds, batch_size=batch_size, padding_id=tokenizer.pad_token_id)
    prefetcher = dataloader.prefetch(n_workers)

    for step, batch in enumerate(prefetcher, start=1):
        print(step)