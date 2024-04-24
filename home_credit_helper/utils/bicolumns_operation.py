import pandas as pd
import numpy as np


def get_dpd(days_entry_payment: pd.Series, days_installment: pd.Series) -> pd.Series:
    dpd = days_entry_payment - days_installment
    dpd = np.where(dpd > 0, dpd, 0)
    return dpd


def get_dbd(days_installment: pd.Series, days_entry_payment: pd.Series) -> pd.Series:
    dbd = days_installment - days_entry_payment
    dbd = np.where(dbd > 0, dbd, 0)
    return dbd
