import pandas as pd
import numpy as np

from home_credit_helper.config import HomeCreditRunnerConfigs
from home_credit_helper.constant import (
    ALL_TABLE_NAMES,
    APPLICATIONS,
    BUREAU_BALANCES,
    BUREAU_KEY,
    BUREAUS,
    CC_BALANCES,
    INSTALLMENTS_PAYMENTS,
    POS_CASH_BALANCES,
    PREV_APPS,
    PRIMARY_KEY,
    SPLIT,
    TEST,
    TRAIN,
    PRODUCTION,
)


def get_dfs(
    cfg: HomeCreditRunnerConfigs, table_names: set = ALL_TABLE_NAMES, test_size: float = 0.1
) -> dict[str, pd.DataFrame]:
    dfs = {}

    if APPLICATIONS in table_names:
        df_main = pd.read_csv(cfg.data_path / "application_train.csv", nrows=cfg.load_data_row_nums)
        df_test = pd.read_csv(cfg.data_path / "application_test.csv", nrows=cfg.load_data_row_nums)

        if cfg.relevant_pks:
            df_main = df_main[df_main[PRIMARY_KEY].isin(cfg.relevant_pks)]
            df_test = df_test[df_test[PRIMARY_KEY].isin(cfg.relevant_pks)]

        df_main[SPLIT] = TRAIN
        test_indices = np.random.choice(df_main.index, size=int(test_size * len(df_main)), replace=False)
        df_main.loc[test_indices, SPLIT] = TEST

        df_test[SPLIT] = PRODUCTION
        df_main = pd.concat([df_main, df_test]).reset_index(drop=True)

        if APPLICATIONS in table_names:
            dfs[APPLICATIONS] = df_main

        del df_test
        del df_main

        if not cfg.relevant_pks:
            cfg.relevant_pks = tuple(dfs[APPLICATIONS][PRIMARY_KEY].unique())

    if BUREAUS in table_names or BUREAU_BALANCES in table_names:
        df = pd.read_csv(cfg.data_path / "bureau.csv")
        df = df[df[PRIMARY_KEY].isin(cfg.relevant_pks)]

        if BUREAUS in table_names:
            dfs[BUREAUS] = df

        if BUREAU_BALANCES in table_names:
            relevant_bureau_keys = tuple(dfs[BUREAUS][BUREAU_KEY].unique())

            df = pd.read_csv(cfg.data_path / "bureau_balance.csv")
            df = df[df[BUREAU_KEY].isin(relevant_bureau_keys)]
            dfs[BUREAU_BALANCES] = df

    if PREV_APPS in table_names:
        df = pd.read_csv(cfg.data_path / "previous_application.csv")
        df = df[df[PRIMARY_KEY].isin(cfg.relevant_pks)]
        dfs[PREV_APPS] = df

    if POS_CASH_BALANCES in table_names:
        df = pd.read_csv(cfg.data_path / "POS_CASH_balance.csv")
        df = df[df[PRIMARY_KEY].isin(cfg.relevant_pks)]
        dfs[POS_CASH_BALANCES] = df

    if INSTALLMENTS_PAYMENTS in table_names:
        df = pd.read_csv(cfg.data_path / "installments_payments.csv")
        df = df[df[PRIMARY_KEY].isin(cfg.relevant_pks)]
        dfs[INSTALLMENTS_PAYMENTS] = df

    if CC_BALANCES in table_names:
        df = pd.read_csv(cfg.data_path / "credit_card_balance.csv")
        df = df[df[PRIMARY_KEY].isin(cfg.relevant_pks)]
        dfs[CC_BALANCES] = df

    return dfs
