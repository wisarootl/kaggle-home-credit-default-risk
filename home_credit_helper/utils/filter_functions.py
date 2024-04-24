import pandas as pd


def bureaus_credit_active_filter_function(df: pd.DataFrame) -> pd.Series:
    return df["CREDIT_ACTIVE_ACTIVE"] == 1


def bureaus_credit_closed_filter_function(df: pd.DataFrame) -> pd.Series:
    return df["CREDIT_ACTIVE_CLOSED"] == 1


def prev_apps_approved_filter_function(df: pd.DataFrame) -> pd.Series:
    return df["NAME_CONTRACT_STATUS_APPROVED"] == 1


def prev_apps_refused_filter_function(df: pd.DataFrame) -> pd.Series:
    return df["NAME_CONTRACT_STATUS_REFUSED"] == 1
