import pandas as pd
import numpy as np

def manipulate_testdata(xtrain, xtest, variable):
    # create xtest_rm
    xtest_rm = xtest.copy()

    # define types of cat_features
    cat_variables = ['object', 'category']

    # replace variable with mode or mean based on its type
    if variable not in cat_variables:
        mean_value = xtrain[variable].mean()
        xtest_rm[variable] = mean_value
    else:
        mode_value = xtrain[variable].mode()[0]
        xtest_rm[variable] = mode_value
    return xtest_rm

def check_method(method):
    """Validate the method parameter."""
    if method not in ["single", "group"]:
        raise ValueError("method parameter must be either 'single' or 'group'")

def convert_to_dataframe(*args):
    """Convert inputs to DataFrames."""
    return [pd.DataFrame(arg).reset_index(drop=True) for arg in args]

def validate_variables(variables, xtrain):
    """Check if variables are valid and exist in the train dataset."""
    if not isinstance(variables, list):
        raise ValueError("Variables input must be a list")
    for var in variables:
        if var not in xtrain.columns:
            raise ValueError(f"{var} is not in the variables")
