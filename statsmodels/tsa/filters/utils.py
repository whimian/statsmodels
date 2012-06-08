from statsmodels.tools.data import _is_using_pandas
from statsmodels.tsa.base import datetools

def _maybe_get_pandas_wrapper(X, trim=None):
    """
    If using pandas returns a function to wrap the results, e.g., wrapper(X)
    trim is an integer for the symmetric truncation of the series in some
    filters.
    otherwise returns None
    """
    if _is_using_pandas(X, None):
        index = X.index
        if trim is not None:
            index = X.index[trim:-trim]
        if hasattr(X, "columns"):
            return lambda x : X.__class__(x, index=index, columns=X.columns)
        else:
            return lambda x : X.__class__(x, index=index, name=X.name)
    else:
        return


def _maybe_get_pandas_wrapper_freq(X, trim=None):
    if _is_using_pandas(X, None):
        index = X.index
        if not datetools._is_datetime_index(index):
            raise ValueError("Index does not contain datetime.datetime or "
                             "is not a pandas timeseries Index")
        func = _maybe_get_pandas_wrapper(X, trim)
        freq = index.inferred_freq
        return func, freq
    else:
        return None, None
