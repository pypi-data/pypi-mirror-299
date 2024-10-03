import pandas as pd
import numpy as np
from .core import rga
from .util.utils import manipulate_testdata, convert_to_dataframe


def compute_rga_parity(xtrain, xtest, ytest, yhat, model, protectedvariable):

    if protectedvariable not in xtrain.columns:
        raise ValueError(f"{protectedvariable} is not in the variables")
    xtrain, xtest, ytest, yhat = convert_to_dataframe(xtrain, xtest, ytest, yhat)
    protected_groups = xtrain[protectedvariable].value_counts().index
    rgas = []
    for i in protected_groups:
        xtest_pr = xtest[xtest[protectedvariable]== i]
        ytest_pr = ytest.loc[xtest_pr.index]
        yhat_pr = [x[1] for x in model.predict_proba(xtest_pr)]
        rga_value = rga(ytest_pr, yhat_pr)
        rgas.append(rga_value)            
    return f"The RGA-based imparity between the protected gorups is {max(rgas)-min(rgas)}."    
    
def compute_single_rgf(xtrain, xtest, ytest, yhat, model, protectedvariable):
 
    if protectedvariable not in xtrain.columns:
        raise ValueError(f"{protectedvariable} is not in the variables")
    xtrain, xtest, ytest, yhat = convert_to_dataframe(xtrain, xtest, ytest, yhat)
    xtest_pr = manipulate_testdata(xtrain, xtest, protectedvariable)
    yhat_pr = [x[1] for x in model.predict_proba(xtest_pr)]
    rgf_value = rga(yhat, yhat_pr)
    return pd.DataFrame(rgf_value, index=[protectedvariable], columns=["RGF"])

