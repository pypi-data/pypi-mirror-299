from ..utils import *

class Transformer:
    def __init__(self, dataset, cols):
        self.dataset = dataset
        if cols is None:
            cols = dataset.columns.tolist()
        self.cols = cols

    def cFilter(self, filters, rindex):
        mask = ~self.dataset[self.cols].apply(filter_row, axis=1, args=(filters,))
        if rindex:
            return self.dataset[mask].reset_index(drop=True)
        return self.dataset[mask]
