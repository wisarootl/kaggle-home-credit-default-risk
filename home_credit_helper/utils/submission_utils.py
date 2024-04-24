from ml_assemblr.main_components.data_pod import DataPod
from home_credit_helper.config import HomeCreditRunnerConfigs


def prepare_submission_files(dp: DataPod, cfg: HomeCreditRunnerConfigs):
    key_col_name = dp.main_column_type.keys[0]
    pred_col_name = dp.main_column_type.predictions[0]
    df = dp.slice_df("production", [key_col_name, pred_col_name])
    df = df.rename(columns={"PRED_TARGET": "TARGET"})
    df.to_csv(cfg.submission_path, index=False)
