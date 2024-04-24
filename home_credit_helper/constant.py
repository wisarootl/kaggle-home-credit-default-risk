from ml_assemblr.main_components.constant import (
    MAIN,
    TRAIN,
    VALID,
    TEST,
    PRODUCTION,
    SPLIT,
)

from ml_assemblr.utils.string_case_utils import to_screaming_snake_case

# table names
APPLICATIONS = "applications"
BUREAUS = "bureaus"
BUREAU_BALANCES = "bureau_balances"
PREV_APPS = "previous_applications"
POS_CASH_BALANCES = "pos_cash_balances"
INSTALLMENTS_PAYMENTS = "installments_payments"
CC_BALANCES = "credit_card_balances"

ALL_TABLE_NAMES = {
    APPLICATIONS,
    BUREAUS,
    BUREAU_BALANCES,
    PREV_APPS,
    PREV_APPS,
    POS_CASH_BALANCES,
    INSTALLMENTS_PAYMENTS,
    CC_BALANCES,
}

# table keys
PRIMARY_KEY = "SK_ID_CURR"
BUREAU_KEY = "SK_ID_BUREAU"

# Column nams
LABEL = "TARGET"

# clean column names for project
SPLIT = to_screaming_snake_case(SPLIT)
