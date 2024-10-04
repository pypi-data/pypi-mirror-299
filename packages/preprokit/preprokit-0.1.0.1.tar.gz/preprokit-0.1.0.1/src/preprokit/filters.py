from sklearn.base import BaseEstimator, TransformerMixin

from .utils import *
from .trasformers import *


class CustomFilters(BaseEstimator, TransformerMixin):
    def __init__(self, cols=None, filters=None, simple=False, reset_index=False):
        """
        Initializes the CustomFilters class with specified parameters.

        Parameters:
            :param cols (list, optional):
                List of column names to apply filters on. Defaults to None.

            :param filters (callable, optional):
                Custom filter function to be applied. Defaults to None.

            :param simple (bool, optional):
                Flag to determine if simple punctuation filters should be used. Defaults to False.

            :param reset_index (bool, optional):
                Flag to determine if the index should be reset after filtering. Defaults to False.
        """
        self.cols = cols
        self._filters(filters, simple)
        self.reset_index = reset_index

    def _filters(self, filters, simple):
        if filters is None and simple:
            self.filters = simple_punctuations
        elif filters is None:
            self.filters = complex_punctuations

    def fit(self, dataset=None):
        """
        Empty fit
        """
        return self

    def transform(self, data):
        """
        Transforms the dataset by applying the specified filters.

        Parameters:
            :param data: The dataObj to be transformed.

        Returns:
            dataObj: The transformed dataObj with filters applied.
        """
        transformer = get_transformer(data, self.cols)
        return transformer.cFilter(self.filters, self.reset_index)
