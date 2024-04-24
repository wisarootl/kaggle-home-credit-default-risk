from ml_assemblr.main_components.data_pod import DataPod
from typing import Optional
from sklearn.metrics import roc_auc_score, root_mean_squared_error
from home_credit_helper.constant import TRAIN, VALID, TEST
import pandas as pd
import shap
import xgboost as xgb
from ml_assemblr.transfromer.model.base_model import get_model_index, get_trained_model
import numpy as np


def calculate_evaluation_metric(df: pd.DataFrame, label_col_name: str, pred_col_name: str, metric: str):
    if metric == "auroc":
        score = roc_auc_score(df[label_col_name], df[pred_col_name])
    elif metric == "rmse":
        score = root_mean_squared_error(df[label_col_name], df[pred_col_name])
    else:
        score = None
    return score


def get_df_cv_evaluation(dp: DataPod, is_cv: bool, cv_idx: Optional[int] = None):
    label_col_name = dp.main_column_type.labels[0]

    if is_cv:
        pred_col_idx_in_col_type = dp.variables["cv_idx_map"]["cv_pred_idx_in_column_type"][cv_idx]
        pred_col_name = dp.main_column_type.predictions[pred_col_idx_in_col_type]
    else:
        pred_col_name = dp.main_column_type.predictions[0]

    metrics = ("auroc",)
    splits = (TRAIN, VALID, TEST)

    cv_evaluation = []

    for metric in metrics:
        for split in splits:
            if is_cv:
                split_idx_in_column_type = dp.variables["cv_idx_map"]["cv_split_idx_in_column_type"][
                    cv_idx
                ]
            else:
                split_idx_in_column_type = 0

            relevant_df = dp.slice_df(
                split=split,
                columns=[pred_col_name, label_col_name],
                table_name=dp.main_df_name,
                split_idx_in_column_type=split_idx_in_column_type,
            )

            if relevant_df.shape[0] > 0:
                metric_value = calculate_evaluation_metric(
                    relevant_df, label_col_name, pred_col_name, metric
                )
            else:
                metric_value = None

            value_col_name = f"value_cv_{cv_idx}" if is_cv else "value"
            cv_evaluation.append({"metric": f"{metric}_{split}", value_col_name: metric_value})

    df_cv_evaluation = pd.DataFrame(cv_evaluation)
    return df_cv_evaluation


def get_shap_values(dp: DataPod, is_cv: bool, cv_idx: int = 1):
    splits = (TRAIN, VALID, TEST)
    shap_results = {}
    for split in splits:
        if is_cv:
            split_idx_in_column_type = dp.variables["cv_idx_map"]["cv_split_idx_in_column_type"][cv_idx]
        else:
            split_idx_in_column_type = 0

        relevant_df_features = dp.slice_df(
            split=split,
            columns="features",
            table_name=dp.main_df_name,
            split_idx_in_column_type=split_idx_in_column_type,
        )

        if relevant_df_features.shape[0] > 0:

            dfeatures = xgb.DMatrix(relevant_df_features)
            model_index = get_model_index(dp, cv_idx=cv_idx)
            booster = get_trained_model(dp, model_index)
            explainer = shap.TreeExplainer(booster)
            shap_values = explainer.shap_values(dfeatures)

            shap_importance = np.mean(abs(shap_values), axis=0)
            feature_names = dp.main_column_type.features
            shap_importance = dict(zip(feature_names, shap_importance, strict=True))
            value_col_name = f"value_cv_{cv_idx}" if is_cv else "value"
            df_shap_importance = pd.DataFrame(
                list(shap_importance.items()), columns=["feature", value_col_name]
            )

            df_shap_importance[value_col_name] = (
                df_shap_importance[value_col_name] / df_shap_importance[value_col_name].sum()
            ) * 100

        else:
            shap_values = None
            df_shap_importance = None

        shap_results[split] = {"shape_value": shap_values, "df_shap_importance": df_shap_importance}

    return shap_results
