from typing import Optional

import numpy as np
from sonusai.mixture import GeneralizedIDs
from sonusai.mixture import MixtureDatabase
from torch.utils.data import Dataset
from torch.utils.data import Sampler

from .dataloader_utils import AawareDataLoader


class MixtureDatabaseDataset(Dataset):
    """Generates a PyTorch dataset from a SonusAI mixture database
    """

    def __init__(self,
                 mixdb: MixtureDatabase,
                 mixids: GeneralizedIDs,
                 cut_len: int,
                 flatten: bool,
                 add1ch: bool,
                 random_cut: bool = True):
        """Initialization
        """
        self.mixdb = mixdb
        self.mixids = self.mixdb.mixids_to_list(mixids)
        self.cut_len = cut_len
        self.flatten = flatten
        self.add1ch = add1ch
        self.random_cut = random_cut

    def __len__(self):
        return len(self.mixids)

    def __getitem__(self, idx: int) -> tuple[np.ndarray, np.ndarray, int]:
        """Get data from one mixture
        """
        import random

        from sonusai.utils import reshape_inputs

        feature, truth = self.mixdb.mixture_ft(self.mixids[idx])
        feature, truth = reshape_inputs(feature=feature,
                                        truth=truth,
                                        batch_size=1,
                                        timesteps=0,
                                        flatten=self.flatten,
                                        add1ch=self.add1ch)

        length = feature.shape[0]

        if self.cut_len > 0:
            if length < self.cut_len:
                feature_final = []
                truth_final = []
                for _ in range(self.cut_len // length):
                    feature_final.append(feature)
                    truth_final.append(truth)
                feature_final.append(feature[: self.cut_len % length])
                truth_final.append(truth[: self.cut_len % length])
                feature = np.vstack([feature_final[i] for i in range(len(feature_final))])
                truth = np.vstack([truth_final[i] for i in range(len(truth_final))])
            else:
                if self.random_cut:
                    start = random.randint(0, length - self.cut_len)
                else:
                    start = 0
                feature = feature[start:start + self.cut_len]
                truth = truth[start:start + self.cut_len]

        return feature, truth, idx


def TorchFromMixtureDatabase(mixdb: MixtureDatabase,
                             mixids: GeneralizedIDs,
                             batch_size: int,
                             flatten: bool,
                             add1ch: bool,
                             num_workers: int = 0,
                             cut_len: int = 0,
                             drop_last: bool = False,
                             shuffle: bool = False,
                             random_cut: bool = True,
                             sampler: Optional[type[Sampler]] = None,
                             pin_memory: bool = False) -> AawareDataLoader:
    """Generates a PyTorch dataloader from a SonusAI mixture database
    """
    from .dataloader_utils import collate_fn

    dataset = MixtureDatabaseDataset(mixdb=mixdb,
                                     mixids=mixids,
                                     cut_len=cut_len,
                                     flatten=flatten,
                                     add1ch=add1ch,
                                     random_cut=random_cut)

    if sampler is not None:
        my_sampler = sampler(dataset)
    else:
        my_sampler = None

    if cut_len == 0 and batch_size > 1:
        result = AawareDataLoader(dataset=dataset,
                                  batch_size=batch_size,
                                  pin_memory=pin_memory,
                                  shuffle=shuffle,
                                  sampler=my_sampler,
                                  drop_last=drop_last,
                                  num_workers=num_workers,
                                  collate_fn=collate_fn)
    else:
        result = AawareDataLoader(dataset=dataset,
                                  batch_size=batch_size,
                                  pin_memory=pin_memory,
                                  shuffle=shuffle,
                                  sampler=my_sampler,
                                  drop_last=drop_last,
                                  num_workers=num_workers)

    result.cut_len = cut_len

    return result
