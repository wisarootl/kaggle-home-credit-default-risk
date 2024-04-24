from ml_assemblr.transfromer.cleaner.categorical_cleaner import CategoricalCleaner
from home_credit_helper.constant import APPLICATIONS
from ml_assemblr.main_components.constant import SPLIT


categorical_cleaner = CategoricalCleaner(
    target_df_name=APPLICATIONS,
    clean_categorical_columns_from_data_inference=True,
    exclude_columns_from_inference={SPLIT},
)

cleaning_pipeline = [categorical_cleaner]
