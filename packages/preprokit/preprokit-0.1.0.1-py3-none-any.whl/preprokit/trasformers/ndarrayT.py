from ..utils import *
import numpy as np

class Transformer:
    def __init__(self, dataset):
        self.dataset = dataset

    def cFilter(self, filters, *args):
        return self.dataset[np.apply_along_axis(lambda row: not filter_row(row, filters), axis=1, arr=self.dataset)]
