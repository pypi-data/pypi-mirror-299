import os
import argparse
import pandas as pd
import torch
from torch import nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, random_split
import time
import random
from tqdm import tqdm
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import adjusted_rand_score,accuracy_score,f1_score,recall_score,precision_score
from pathlib import Path
from collections import Counter
import os
import tracemalloc
from sklearn.metrics import balanced_accuracy_score


def display_top(snapshot, key_type='lineno', limit=3):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        # replace "/path/to/module/file.py" with "module/file.py"
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        print("#%s: %s:%s: %.1f KiB"
              % (index, filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))


def seed_all(seed_value, cuda_deterministic=False):
    print('---------------------------------- SEED ALL ---------------------------------- ')
    print(f'                           Seed Num :   {seed_value}                                ')
    print('---------------------------------- SEED ALL ---------------------------------- ')
    random.seed(seed_value)
    os.environ['PYTHONHASHSEED'] = str(seed_value)
    np.random.seed(seed_value)
    torch.manual_seed(seed_value)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed_value)
        torch.cuda.manual_seed_all(seed_value) # Speed-reproducibility tradeoff https://pytorch.org/docs/stable/notes/randomness.html
        if cuda_deterministic: # slower, more reproducible
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
        else: # faster, less reproducible
            torch.backends.cudnn.deterministic = False
            torch.backends.cudnn.benchmark = True

