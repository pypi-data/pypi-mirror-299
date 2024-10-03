import numpy as np

def pad_parameters(dataset, missing_params=[], desired_params=None, axis=-1):
    """
    Pads columns with NaNs in desired places. If `desired_params` is None,
    padded columns are appended at the end.
    
    Parameters
    ----------
    dataset: array
        dataset to be padded
    axis: int
        axis along which to add padded columns
    missing_params: list
        a list of parameter names present in `desired_params`, but for which
        entries are missing from `dataset`
    desired_params: list
        a list of all desired parameter names, both present and missing
    """
    padded_dataset = np.copy(dataset)
    
    if desired_params is None:
        idx = [dataset.shape[axis]+i for i in range(len(missing_params))]
    else:
        if dataset.shape[axis] + len(missing_params) < len(desired_params):
            raise Exception('not enough missing parameters given')
        if dataset.shape[axis] + len(missing_params) > len(desired_params):
            raise Exception('too many missing parameters given')
        idx = np.argwhere(np.in1d(desired_params, missing_params)).flatten()
    
    for i in idx:
        padded_dataset = np.insert(padded_dataset, i, np.nan, axis=axis)
    return padded_dataset
